from .base import BaseAdapter
from .github import GithubAdapter
from .intercom import IntercomAdapter
from .zendesk import ZendeskAdapter

_REGISTRY: dict[str, BaseAdapter] = {
    "github": GithubAdapter(),
    "intercom": IntercomAdapter(),
    "zendesk": ZendeskAdapter(),
}

def get_adapter(name: str) -> BaseAdapter | None:
    return _REGISTRY.get(name)
