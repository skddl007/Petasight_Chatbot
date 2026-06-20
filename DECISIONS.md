# DECISIONS.md

## The three rules — how they are defined

The brief requires checking rules **in order; first match wins**. Classification lives in `backend/app/input_classifier.py`; colors in `backend/app/color_engine.py`.

| Order | Rule | When it applies | Bubble color |
|-------|------|-----------------|--------------|
| 1 | **City + temperature** | Message matches a city paired with a Celsius temperature | Deep blue → light purple → bright red |
| 2 | **Standalone decimal** | No Rule 1 match, but a decimal number is present | Sepia ramp (`.00` lightest → `.99` darkest) |
| 3 | **Panic / mood** | Neither Rule 1 nor Rule 2 matches | Violet (panic) → magenta → pale yellow (calm) |

---

### Rule 1 — City + temperature in Celsius

**Brief:** *"A city and a temperature in Celsius."*

**Detection** — message must match one of these patterns (regex in `input_classifier.py`):

1. **City then temp:** `Mumbai 32`, `Delhi 15C`, `London 28°C`, `Paris -5`
   - City name (letters, spaces, hyphens, apostrophes) immediately followed by a number
   - Optional `°`, `C`, or `celsius` after the number

2. **Temp then city:** `32C in Berlin`, `28°C in London`
   - Number + `C`/`celsius` + `in` / `at` / `for` + city name

3. **Degrees phrasing:** `it's 20 degrees in Paris`, `20 degree in Tokyo`
   - Optional `it's` + number + `degree(s)` + `in` / `at` / `for` + city name

**Does not match Rule 1:**
- City alone (`Mumbai`) or integer alone (`32`)
- Number and city in the same sentence but **not paired as weather** — e.g. `"My rating is 0.42 in Mumbai"` (rating, not °C; city not adjacent to temp)
- Messages with no recognizable city+temp pattern

**Color mapping** (`temp_to_rgb`):

| Temperature | Color |
|-------------|--------|
| ≤ 0°C | Deep blue `rgb(0, 0, 139)` |
| 0°C → 15°C | Linear blend deep blue → light purple `rgb(200, 160, 230)` |
| 15°C | Light purple (anchor) |
| 15°C → 35°C | Linear blend light purple → bright red `rgb(220, 20, 20)` |
| ≥ 35°C | Bright red |

**Examples:** `Mumbai 32` → Rule 1, ~red; `Delhi 0` → deep blue; `London 15` → light purple.

**Reply:** Groq LLM (Ibn Sina persona) — coloring only depends on the detected temperature.

---

### Rule 2 — Standalone decimal

**Brief:** *"Otherwise, a standalone decimal number."*

**Detection** — first decimal in the message matching:

```
(?:^|(?<!\d))(\.\d+|\d+\.\d+)(?!\d)
```

- Matches: `3.14`, `0.42`, `.75`, `.5`, `0.99`
- **Requires a decimal point** — bare `32` does not match (falls to Rule 3)
- **Negative decimals excluded** — `-0.5` is skipped (the `-` before the match disqualifies it)
- If multiple decimals exist, the **first** one wins (e.g. `3.14 2.71` → uses `.14`)

**Digit extraction for color:**
- Take the **first two digits after the decimal point**, zero-padded on the right
- `.5` → `50`, `3.14` → `14`, `0.00` → `00`, `0.99` → `99`
- Map 00–99 to a **sepia** ramp: `.00` lightest beige, `.99` darkest brown

**Examples:** `0.42` → Rule 2, sepia from digits `42`; `3.14` → sepia from `14`.

**Reply:** Groq LLM (Ibn Sina persona) — coloring only depends on the decimal digits.

---

### Rule 3 — LLM panic score (everything else)

**Brief:** *"Otherwise, ask the LLM how urgent or panicked the message sounds."*

**Detection** — fallback when Rule 1 and Rule 2 both fail.

**Examples that reach Rule 3:**
- Plain text: `HELP ME NOW`, `hello`, `what's the weather?`
- City only: `Mumbai`
- Integer only: `32`
- Negative decimal: `-0.5`

**Panic scoring** — Groq returns JSON with `panic_score` from **0.0** (completely calm) to **1.0** (extreme panic), based on how urgent the message sounds.

**Color mapping** (`panic_to_rgb`):

| Panic score | Color |
|-------------|--------|
| 0.0 | Pale yellow `rgb(255, 255, 200)` — calm |
| 0.0 → 0.5 | Blend pale yellow → magenta |
| 0.5 | Magenta `rgb(255, 0, 255)` |
| 0.5 → 1.0 | Blend magenta → violet |
| 1.0 | Violet `rgb(138, 43, 226)` — high panic |

**Reply:** Groq LLM (Ibn Sina persona) + panic score in one JSON call.

---

## What happens when a message has both a city+temp and a standalone decimal?

The brief deliberately leaves this open-ended and says not to ask — just pick something and explain it.

**Decision: strict priority order, first match wins.** If Rule 1 matches, the bubble is colored by temperature. The decimal is ignored for coloring, even if it appears in the same message.

| Message | Rule | Why |
|---------|------|-----|
| `Mumbai 32.5` | Rule 1 | City+temp pair; `32.5` is Celsius, not a standalone decimal for coloring |
| `Mumbai 32 and rating 0.42` | Rule 1 | `Mumbai 32` matches before decimal scan |
| `0.42` | Rule 2 | No city+temp pattern |
| `My rating is 0.42 in Mumbai` | Rule 2 | No city+temp pair; `0.42` is a rating, not weather |

Verified: `test_rule1_wins_over_decimal` and live API on `"Mumbai 32 and rating 0.42"` → Rule 1.

---

## City + temperature: parse from the message, no weather API

The brief describes Rule 1 as triggering on *"a city and a temperature in Celsius"* in the message — not live weather lookup. A weather API would introduce ambiguity (typed `32` vs actual `28°C`) and extra scope.

---

## Rule 2 color ramp: sepia over grayscale

The brief allows *"Grayscale or sepia."* Sepia was chosen for visual separation from Rule 1’s blue–purple–red spectrum and Rule 3’s violet–magenta–yellow range.

---

## Rule 1 color mapping — brief, not the review file

Production `color_engine.py` follows the brief directly. The buggy `public/review/color_cache.py` uses wrong interpolation for 15–35°C — see `REVIEW.md`. `test_fifteen_is_light_purple` confirms the 15°C anchor.

---

## Text readability on dynamic backgrounds

`textColor` is computed server-side from background luminance (WCAG formula) and returned with every reply so text stays readable on all three rule color ranges.

---

## LLM choice: Groq with llama-3.3-70b-versatile

Real LLM for all replies (not canned). Rule 3 uses structured JSON with `panic_score`; Rules 1–2 use the same LLM for chat with bilingual Ibn Sina output.

---

## Auth design

Email + password with JWT. Backend enforces `@petasight.com` on register, login, `/auth/me`, and `/chat`.

---

## Bonus: Ibn Sina speaking Arabic

Replies in Arabic (RTL) as Ibn Sina, then English translation. JSON fields `original` + `translation`; frontend sets `dir="rtl"` on Arabic text.

---

## Verification summary

| Check | Status |
|-------|--------|
| Backend pytest (37 tests) | Pass |
| Rule 1 / 2 / 3 classification and colors | Pass |
| First-match ambiguity | Rule 1 wins when both patterns present |
| `@petasight.com` backend enforcement | Pass |
| Groq LLM (not canned) | Pass |
| Keyboard navigation and contrast | Pass |
| Live deployment | [Frontend](https://petasight-chatbot.vercel.app) · [API](https://petasight-chatbot-api.onrender.com) |
