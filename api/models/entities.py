from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, JSON, Integer
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
try:
    from pgvector.sqlalchemy import Vector
except Exception:  # fallback type hint
    class Vector:  # type: ignore
        def __init__(self, *_: int, **__: str) -> None: ...
from models.db import Base
from sqlalchemy import Boolean


class KbCard(Base):
    __tablename__ = "kb_cards"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=False, default=list)
    embedding: Mapped[list[float] | None] = mapped_column(ARRAY(Float), nullable=True)
    # New pgvector column; keep array for backward-compat
    embedding_vec: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)  # type: ignore
    # created_at/updated_at handled by DB defaults in migration


class RefEvent(Base):
    __tablename__ = "ref_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(Text, nullable=False)
    product: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # created_at handled by DB default


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    ref_event_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="draft")
    # created_at/updated_at handled by DB defaults


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    ticket_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # created_at handled by DB default


class ProductSignal(Base):
    __tablename__ = "product_signals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    origin: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    product_area: Mapped[str | None] = mapped_column(Text, nullable=True)
    strength: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    evidence_refs: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=False, default=list)
    # created_at handled by DB default


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    receipt_id: Mapped[str] = mapped_column(Text, nullable=False)
    verified: Mapped[bool] = mapped_column(default=False)
    # created_at handled by DB default


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    roles: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=False, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class BeaconReceipt(Base):
    __tablename__ = "beacon_receipts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    signature: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


