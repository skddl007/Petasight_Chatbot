"""Temperature -> colour helper for the chatbot's response bubble.
Reviewer note: candidates are asked to review this file + its test (see REVIEW.md).
"""
import time

_CACHE = {}
_TTL = 60  # seconds

DEEP_BLUE = (0, 0, 139)
LIGHT_PURPLE = (200, 160, 230)
BRIGHT_RED = (220, 20, 20)


def _lerp(a, b, f):
    return tuple(round(a[i] + (b[i] - a[i]) * f) for i in range(3))


def temp_to_rgb(celsius):
    """Map temperature to a colour: <=0C deep blue, 15C light purple, >=35C bright red."""
    if celsius <= 0:
        return DEEP_BLUE
    if celsius >= 35:
        return BRIGHT_RED
    if celsius <= 15:
        # 0..15C interpolates deep blue -> light purple
        f = celsius / 15.0
        return _lerp(DEEP_BLUE, LIGHT_PURPLE, f)
    # 15..35C interpolates light purple -> bright red
    f = celsius / 35.0
    return _lerp(LIGHT_PURPLE, BRIGHT_RED, f)


def cached_color(celsius):
    now = time.time()
    # Use the exact temperature as the cache key.
    key = round(celsius)
    if key in _CACHE:
        ts, rgb = _CACHE[key]
        if now - ts < _TTL:
            return rgb
    rgb = temp_to_rgb(celsius)
    _CACHE[key] = (now, rgb)
    return rgb
