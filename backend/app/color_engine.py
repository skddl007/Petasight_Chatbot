"""Bubble color mapping per brief.md lines 11-13."""

DEEP_BLUE = (0, 0, 139)
LIGHT_PURPLE = (200, 160, 230)
BRIGHT_RED = (220, 20, 20)

VIOLET = (138, 43, 226)
MAGENTA = (255, 0, 255)
PALE_YELLOW = (255, 255, 200)


def _lerp(a: tuple[int, int, int], b: tuple[int, int, int], f: float) -> tuple[int, int, int]:
    return tuple(round(a[i] + (b[i] - a[i]) * f) for i in range(3))


def temp_to_rgb(celsius: float) -> tuple[int, int, int]:
    """Rule 1: deep blue at 0 or below, light purple around 15, bright red at 35 or above."""
    if celsius <= 0:
        return DEEP_BLUE
    if celsius >= 35:
        return BRIGHT_RED
    if celsius <= 15:
        f = celsius / 15.0
        return _lerp(DEEP_BLUE, LIGHT_PURPLE, f)
    f = (celsius - 15) / 20.0
    return _lerp(LIGHT_PURPLE, BRIGHT_RED, f)


def decimal_to_rgb(two_digit_value: int) -> tuple[int, int, int]:
    """Rule 2: sepia ramp from first two decimal digits; .00 lightest, .99 darkest."""
    t = max(0, min(99, two_digit_value)) / 99.0
    r = round(245 - t * 185)
    g = round(240 - t * 195)
    b = round(230 - t * 200)
    return (r, g, b)


def panic_to_rgb(score: float) -> tuple[int, int, int]:
    """Rule 3: violet for high panic, through magenta, to pale yellow for calm."""
    score = max(0.0, min(1.0, score))
    if score >= 0.5:
        f = (score - 0.5) / 0.5
        return _lerp(MAGENTA, VIOLET, f)
    f = score / 0.5
    return _lerp(PALE_YELLOW, MAGENTA, f)


def rgb_to_css(rgb: tuple[int, int, int]) -> str:
    return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"


def text_color_for_bg(rgb: tuple[int, int, int]) -> str:
    luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    return "#000000" if luminance > 186 else "#ffffff"
