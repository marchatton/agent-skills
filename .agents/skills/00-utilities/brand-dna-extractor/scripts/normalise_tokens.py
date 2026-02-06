"""
normalise_tokens.py

Helpers to normalise common style values:
- rgb/rgba to hex
- parse px values from spacing strings
- infer spacing step (4px/8px) from observed paddings/margins

Keep deterministic. Avoid guessing when parsing fails.
"""

from __future__ import annotations

import re
from typing import Iterable, Optional, List

RGB_RE = re.compile(
    r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*([0-9.]+))?\s*\)",
    re.IGNORECASE,
)
PX_RE = re.compile(r"(-?\d+(?:\.\d+)?)px")

def clamp_byte(n: int) -> int:
    return max(0, min(255, n))

def rgb_to_hex(value: str) -> Optional[str]:
    """Convert rgb/rgba string to #RRGGBB. Ignores alpha."""
    m = RGB_RE.fullmatch(value.strip())
    if not m:
        return None
    r, g, b = (clamp_byte(int(m.group(i))) for i in (1, 2, 3))
    return f"#{r:02X}{g:02X}{b:02X}"

def extract_px_numbers(value: str) -> List[float]:
    """Extract numeric px values from a CSS shorthand string."""
    return [float(x) for x in PX_RE.findall(value)]

def infer_spacing_step(px_values: Iterable[float]) -> Optional[int]:
    """Infer spacing base step from observed px values."""
    ints = [abs(int(round(v))) for v in px_values if v is not None]
    ints = [v for v in ints if v != 0 and v <= 256]
    if len(ints) < 6:
        return None

    div4 = sum(1 for v in ints if v % 4 == 0)
    div8 = sum(1 for v in ints if v % 8 == 0)

    if div8 / len(ints) >= 0.7:
        return 8
    if div4 / len(ints) >= 0.7:
        return 4
    return None
