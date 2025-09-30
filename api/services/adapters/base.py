from typing import Dict, Any, Protocol, Optional
import time
import httpx


class BaseAdapter(Protocol):
    name: str
    def perform(self, payload: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> str: ...


def http_post_with_retries(url: str, json_body: Dict[str, Any], headers: Dict[str, str], timeout: float = 10.0, retries: int = 2, backoff: float = 0.5) -> httpx.Response:
    last_err: Exception | None = None
    for i in range(retries + 1):
        try:
            with httpx.Client(timeout=timeout) as client:
                r = client.post(url, json=json_body, headers=headers)
                r.raise_for_status()
                return r
        except Exception as e:
            last_err = e
            if i < retries:
                time.sleep(backoff * (2 ** i))
            else:
                raise
    # Unreachable, but keeps type checkers happy
    if last_err:
        raise last_err
    raise RuntimeError("unexpected adapter error")

