import pytest

from app.input_classifier import classify_input, preprocess_message


@pytest.mark.parametrize(
    "message,expected_rule,expected_key",
    [
        ("Mumbai 32", "city_temp", "celsius"),
        ("Delhi 15C", "city_temp", "celsius"),
        ("London 28°C", "city_temp", "celsius"),
        ("32C in Berlin", "city_temp", "celsius"),
        ("it's 20 degrees in Paris", "city_temp", "celsius"),
        ("Mumbai 32.5", "city_temp", "celsius"),
        ("Mumbai -5", "city_temp", "celsius"),
    ],
)
def test_rule1_city_temp(message, expected_rule, expected_key):
    rule, meta = classify_input(message)
    assert rule == expected_rule
    assert expected_key in meta


@pytest.mark.parametrize(
    "message",
    ["Mumbai", "32"],
)
def test_falls_to_panic(message):
    rule, _ = classify_input(message)
    assert rule == "panic"


@pytest.mark.parametrize(
    "message,expected_fraction",
    [
        ("3.14", 0.14),
        ("0.99", 0.99),
        ("0.00", 0.00),
        (".75", 0.75),
        (".5", 0.50),
    ],
)
def test_rule2_decimal(message, expected_fraction):
    rule, meta = classify_input(message)
    assert rule == "decimal"
    assert meta["fraction"] == expected_fraction


def test_rule1_wins_over_decimal():
    rule, meta = classify_input("Mumbai 32.5")
    assert rule == "city_temp"
    assert meta["celsius"] == 32.5


def test_negative_decimal_falls_to_panic():
    rule, _ = classify_input("-0.5")
    assert rule == "panic"


def test_first_decimal_wins():
    rule, meta = classify_input("3.14 2.71")
    assert rule == "decimal"
    assert meta["fraction"] == 0.14


def test_preprocess_empty():
    assert preprocess_message("   ") == ""


def test_preprocess_truncates():
    long_msg = "a" * 1000
    assert len(preprocess_message(long_msg)) == 500
