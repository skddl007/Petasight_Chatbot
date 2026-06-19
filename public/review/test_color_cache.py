from color_cache import temp_to_rgb, cached_color


def test_freezing_is_deep_blue():
    assert temp_to_rgb(-5) == (0, 0, 139)


def test_hot_is_bright_red():
    assert temp_to_rgb(40) == (220, 20, 20)


def test_returns_a_tuple():
    assert isinstance(temp_to_rgb(25), tuple)


def test_cache_runs():
    cached_color(20)
    assert True
