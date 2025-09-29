from typing import List

def embed_text(text: str) -> List[float]:
    # Increase dimension to better approximate real vector behavior; deterministic hash-based embedding
    dims = 64
    v = [0.0] * dims
    for idx, ch in enumerate(text or ""):
        v[idx % dims] += (ord(ch) % 29) / 31.0
    # L2 normalize
    norm = sum(x * x for x in v) ** 0.5 or 1.0
    return [x / norm for x in v]
