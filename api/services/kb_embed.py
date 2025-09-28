from typing import List

def embed_text(text: str) -> List[float]:
    dims = 16
    v = [0.0] * dims
    for idx, ch in enumerate(text or ""):
        v[idx % dims] += (ord(ch) % 13) / 10.0
    return v
