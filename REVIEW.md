# REVIEW.md

I went through both files and found two bugs in color_cache.py.


# Bug 1: color_cache.py, temp_to_rgb function

The issue is in the last part of the function where it handles 15 to 35 degrees:

# f = celsius / 35.0


This is wrong. f here is supposed to say how far we are between 15°C and 35°C, so at 15°C it should be 0.0 and at 35°C it should be 1.0. But dividing by 35 doesn't do that, at 15°C you get 0.43, which means the color is already almost halfway to bright red before it even starts the segment. If you open the app and type something at 14°C then 16°C you did see the color jump, it does not blend smoothly through light purple at all.

The fix is straightforward:

# f = (celsius - 15) / 20.0


Subtract 15 so you are counting from the start of the range, divide by 20 because that's the size of the range (35 minus 15). Now 15°C gives 0.0 and 35°C gives 1.0 and the gradient is smooth.


# Bug 2: color_cache.py, cached_color function

This one is a bit subtle. The cache rounds the temperature to use as a key, but then computes the color from the original unrounded value:

key = round(celsius)
rgb = temp_to_rgb(celsius)   # still using the exact value
_CACHE[key] = (now, rgb)

So if you call cached_color(20.9), it stores that color under key 20. Next call with cached_color(20.1) hits the same key and returns the color for 20.9 instead. The cache is lying about what it stored.

Fix it by computing from the rounded value too:

key = round(celsius)
rgb = temp_to_rgb(key)
_CACHE[key] = (now, rgb)

Now key 20 always holds the color for exactly 20°C, no mismatch.

I also added four tests to test_color_cache.py to cover the 15°C anchor, the boundary continuity, the cache key collision, and a range check the original tests only covered the extremes and missed both bugs entirely.