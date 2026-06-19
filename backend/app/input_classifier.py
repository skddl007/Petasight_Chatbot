import re

CITY_TEMP_PATTERNS = [
    re.compile(
        r"(?P<city>[A-Za-z][A-Za-z\s\-']{0,40}?)\s+"
        r"(?P<temp>-?\d+(?:\.\d+)?)\s*°?\s*(?:C|celsius)?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?P<temp>-?\d+(?:\.\d+)?)\s*°?\s*(?:C|celsius)\s+"
        r"(?:in|at|for)\s+"
        r"(?P<city>[A-Za-z][A-Za-z\s\-']{0,40})",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:it'?s\s+)?(?P<temp>-?\d+(?:\.\d+)?)\s+degrees?\s+"
        r"(?:in|at|for)\s+"
        r"(?P<city>[A-Za-z][A-Za-z\s\-']{0,40})",
        re.IGNORECASE,
    ),
]

DECIMAL_PATTERN = re.compile(r"(?:^|(?<!\d))(\.\d+|\d+\.\d+)(?!\d)")


def _valid_city(city: str) -> bool:
    city = city.strip()
    return bool(city) and any(c.isalpha() for c in city)


def _match_city_temp(message: str) -> dict | None:
    for pattern in CITY_TEMP_PATTERNS:
        match = pattern.search(message)
        if not match:
            continue
        city = match.group("city").strip()
        if not _valid_city(city):
            continue
        return {"city": city, "celsius": float(match.group("temp"))}
    return None


def _extract_decimal_digits(decimal_str: str) -> int:
    fractional = decimal_str.split(".", 1)[1]
    digits = fractional[:2].ljust(2, "0")
    return int(digits)


def _match_decimal(message: str) -> dict | None:
    match = DECIMAL_PATTERN.search(message)
    if not match:
        return None
    start = match.start(1)
    if start > 0 and message[start - 1] == "-":
        return None
    decimal_str = match.group(1)
    two_digit_value = _extract_decimal_digits(decimal_str)
    fraction = two_digit_value / 100.0
    return {"decimal_str": decimal_str, "two_digit_value": two_digit_value, "fraction": fraction}


def classify_input(message: str) -> tuple[str, dict]:
    """Return (rule, meta). Rules: city_temp | decimal | panic."""
    city_temp = _match_city_temp(message)
    if city_temp:
        return "city_temp", city_temp

    decimal = _match_decimal(message)
    if decimal:
        return "decimal", decimal

    return "panic", {}


def preprocess_message(message: str) -> str:
    return message.strip()[:500]
