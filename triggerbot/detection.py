# vibecoded project, i take no credit for it

import unicodedata
from triggers import LEVELS, THRESHOLDS

def normalize(text: str) -> str:
    """Minuscules + suppression des accents."""
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")

def score_message(content: str, level: int) -> tuple[int, list[str]]:
    """Retourne (score_total, catégories_touchées)."""
    text = normalize(content)
    total, hits = 0, []
    for cat, (weight, keywords) in LEVELS[level].items():
        if any(kw in text for kw in keywords):
            hits.append(f"{cat}(+{weight})")
            total += weight
    return total, hits

def get_threshold(level: int) -> int:
    return THRESHOLDS[level]
