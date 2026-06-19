# REVIEW.md

Review of [`public/review/color_cache.py`](public/review/color_cache.py) and [`public/review/test_color_cache.py`](public/review/test_color_cache.py).

---

## Bug 1: Wrong interpolation factor for 15–35°C (lines 28–30)

**What's broken:** The 15–35°C segment uses `f = celsius / 35.0` instead of normalizing over the 15–35 range.

**Why it matters:** At exactly 15°C, `f = 15/35 ≈ 0.43`, so the color is ~43% toward bright red instead of at the light purple anchor. The brief requires *"light purple around 15"* — this formula skips that anchor entirely for the upper segment.

**Fix:**
```python
f = (celsius - 15) / 20.0
return _lerp(LIGHT_PURPLE, BRIGHT_RED, f)
```

**Test to add:** `assert temp_to_rgb(15) == LIGHT_PURPLE`

---

## Bug 2: Cache key contradicts comment (line 36)

**What's broken:** Comment says *"Use the exact temperature as the cache key"* but code uses `round(celsius)`, collapsing nearby values (e.g. 20.1 and 20.4 share key `20`).

**Why it matters:** Different precise temperatures may return a cached color computed for a different value. Misleading comment suggests this is unintentional.

**Fix:** Either use `celsius` directly as key (if exact caching is desired) or update the comment to document intentional rounding for cache efficiency.

---

## Bug 3: No cache eviction

**What's broken:** Stale entries remain in `_CACHE` forever; they are only ignored on read after TTL expires.

**Why it matters:** Memory grows unbounded over long-running processes with many distinct temperatures.

**Fix:** Delete expired entries on read, or run periodic cleanup. For a chatbot with limited temperature range this is minor but worth noting.

---

## Bug 4: Weak test coverage (`test_color_cache.py`)

**What's broken:**
- No test for the 15°C anchor (would catch Bug 1).
- No mid-range temperature assertion (e.g. 25°C).
- `test_cache_runs` only calls `cached_color(20)` and asserts `True` — vacuous, tests nothing.
- No cache hit/miss or TTL expiry tests.

**Fix:** Add tests for 15°C, 25°C, cache hit on second call with same rounded key, and expired TTL returning fresh computation.

---

## Production note

The corrected `temp_to_rgb` implementation lives in [`backend/app/color_engine.py`](backend/app/color_engine.py), following [`public/brief.md`](public/brief.md) line 11 — not the buggy review file.

**Confirmed in production tests:** `test_fifteen_is_light_purple`, `test_thirty_five_is_bright_red`, and live API color output for `"Mumbai 32"` match the brief's anchors (15°C purple, 35°C red).
