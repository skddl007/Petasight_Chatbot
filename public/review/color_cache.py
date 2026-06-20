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

# --- added ---
 
def test_15C_is_light_purple():
    # spec calls this out as a named anchor, and this is where Bug 1 breaks
    assert temp_to_rgb(15) == LIGHT_PURPLE
 
 
def test_color_continuous_at_15C():
    # no visible jump at the boundary between the two segments
    below = temp_to_rgb(14.9)
    above = temp_to_rgb(15.1)
    for a, b in zip(below, above):
        assert abs(a - b) < 5
 
 
def test_cache_key_collision_is_consistent():
    # 20.1 and 20.9 both round to 20, should return same color
    assert cached_color(20.1) == cached_color(20.9)
 
 
def test_rgb_values_in_valid_range():
    # out of range channels break colors silently in the browser
    for temp in range(-10, 45):
        r, g, b = temp_to_rgb(temp)
        assert all(0 <= c <= 255 for c in (r, g, b))