from contextlib import contextmanager
from typing import Iterator, Optional


@contextmanager
def start_span(name: str, attributes: Optional[dict] = None) -> Iterator[None]:
    """Start an OTel span if opentelemetry is installed; otherwise no-op."""
    tracer = None
    span = None
    try:
        from opentelemetry import trace  # type: ignore

        tracer = trace.get_tracer(__name__)
        if tracer:
            span = tracer.start_as_current_span(name)
            if attributes:
                # set attributes after entering span
                ctx = span.__enter__()
                try:
                    current = trace.get_current_span()
                    for k, v in (attributes or {}).items():
                        current.set_attribute(k, v)
                finally:
                    # yield control inside span
                    yield
                    span.__exit__(None, None, None)
                    return
    except Exception:
        pass

    # Fallback: simple no-op context
    yield


