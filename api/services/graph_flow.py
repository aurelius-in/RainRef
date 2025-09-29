from __future__ import annotations

from typing import Any, Dict, List, Tuple, TypedDict
from langgraph.graph import StateGraph, END
import logging
from models.entities import ProductSignal
from sqlalchemy.orm import Session
from models.schemas import RefEventIn, AnswerProposal
from .grounder import retrieve_with_citations, compose_answer
from .policy import check_allow
from .tracing import start_span


class FlowState(TypedDict, total=False):
    ref_event: Dict[str, Any]
    intent: str
    citations: List[Tuple[str, str]]
    answer_md: str
    actions: List[Dict[str, Any]]
    gated: List[Dict[str, Any]]


def _triage(state: FlowState) -> FlowState:
    with start_span("flow.triage"):
        text = (state.get("ref_event", {}).get("text") or "").lower()
        intent = "activation" if "activation" in text else "general"
        state["intent"] = intent
        return state


def _retrieve(db: Session, state: FlowState) -> FlowState:
    with start_span("flow.retrieve"):
        text = state.get("ref_event", {}).get("text") or ""
        cits = retrieve_with_citations(db, text, k=3)
        state["citations"] = cits
        state["answer_md"] = compose_answer(text, cits)
        return state


def _plan(state: FlowState) -> FlowState:
    with start_span("flow.plan"):
        text = (state.get("ref_event", {}).get("text") or "").lower()
        user_ref = state.get("ref_event", {}).get("user_ref")
        actions: List[Dict[str, Any]] = []
        if "activation" in text:
            actions.append({"type": "resend_activation", "params": {"user_ref": user_ref}})
        state["actions"] = actions
        return state


async def _gate(state: FlowState) -> FlowState:
    with start_span("flow.gate"):
        gated: List[Dict[str, Any]] = []
        for a in state.get("actions", []) or []:
            res = await check_allow(a)
            allow = res.get("allow") if isinstance(res, dict) else bool(res)
            gated.append({**a, "allowed": allow, "policy_reason": (res.get("reason") if isinstance(res, dict) else None)})
        state["gated"] = gated
        return state


def _signalize(db: Session, state: FlowState) -> FlowState:
    """Create a basic ProductSignal from the flow outcome (stub)."""
    with start_span("flow.signalize"):
        try:
            intent = state.get("intent") or "general"
            sig = ProductSignal(
                origin=state.get("ref_event", {}).get("source") or "ref",
                type=str(intent),
                product_area=None,
                strength=0.1,
                evidence_refs=[e[0] for e in (state.get("citations") or [])],
            )
            db.add(sig)
            db.commit()
            logging.getLogger(__name__).info("signalized intent=%s id=%s", intent, sig.id)
        except Exception as e:
            logging.getLogger(__name__).warning("signalize failed: %s", e)
            try:
                db.rollback()
            except Exception:
                pass
        return state


def build_graph(db: Session) -> StateGraph:
    sg: StateGraph = StateGraph(FlowState)

    # Node wrappers capture db where needed
    sg.add_node("triage", lambda s: _triage(s))
    sg.add_node("retrieve", lambda s: _retrieve(db, s))
    sg.add_node("plan", lambda s: _plan(s))
    sg.add_node("gate", lambda s: s)  # async not supported directly in builder; gate as preview only
    sg.add_node("signal", lambda s: _signalize(db, s))

    sg.set_entry_point("triage")
    sg.add_edge("triage", "retrieve")
    sg.add_edge("retrieve", "plan")
    sg.add_edge("plan", "gate")
    sg.add_edge("gate", "signal")
    sg.add_edge("signal", END)
    return sg


def run_flow_graph(db: Session, ref_event: RefEventIn) -> Tuple[AnswerProposal, str]:
    graph = build_graph(db)
    state: FlowState = {"ref_event": ref_event.model_dump()}
    out = graph.compile().invoke(state)

    citations = [f"kb:{cid}" for cid, _ in (out.get("citations") or [])]
    proposal = AnswerProposal(
        ticket_id="",
        answer_md=out.get("answer_md") or "",
        citations=citations,
        actions_suggested=out.get("actions") or [],
    )
    return proposal, "graph-receipt"


