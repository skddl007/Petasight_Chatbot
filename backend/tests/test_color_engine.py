import pytest

from app.color_engine import (
    BRIGHT_RED,
    DEEP_BLUE,
    LIGHT_PURPLE,
    PALE_YELLOW,
    VIOLET,
    decimal_to_rgb,
    panic_to_rgb,
    temp_to_rgb,
    text_color_for_bg,
)


def test_freezing_is_deep_blue():
    assert temp_to_rgb(-5) == DEEP_BLUE


def test_zero_is_deep_blue():
    assert temp_to_rgb(0) == DEEP_BLUE


def test_fifteen_is_light_purple():
    assert temp_to_rgb(15) == LIGHT_PURPLE


def test_thirty_five_is_bright_red():
    assert temp_to_rgb(35) == BRIGHT_RED


def test_hot_is_bright_red():
    assert temp_to_rgb(40) == BRIGHT_RED


def test_mid_range():
    rgb = temp_to_rgb(25)
    assert isinstance(rgb, tuple)
    assert len(rgb) == 3


def test_decimal_lightest():
    rgb = decimal_to_rgb(0)
    assert rgb[0] > 200


def test_decimal_darkest():
    rgb = decimal_to_rgb(99)
    assert rgb[0] < 100


def test_panic_high():
    assert panic_to_rgb(1.0) == VIOLET


def test_panic_calm():
    assert panic_to_rgb(0.0) == PALE_YELLOW


def test_text_color_contrast():
    assert text_color_for_bg(DEEP_BLUE) == "#ffffff"
    assert text_color_for_bg(PALE_YELLOW) == "#000000"
