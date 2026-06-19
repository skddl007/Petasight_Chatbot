# DECISIONS.md

## Ambiguity: city+temp AND standalone decimal in one message

**Decision:** Apply rules in strict priority order (Rule 1 → Rule 2 → Rule 3). First match determines bubble color; later patterns are ignored for coloring.

**Examples:**
- `"Mumbai 32.5"` → Rule 1 (`temp_to_rgb(32.5)`). The number is a Celsius temperature paired with a city, not a standalone decimal.
- `"Mumbai 32 and rating 0.42"` → Rule 1 (`temp_to_rgb(32)`). City+temp is detected before the decimal scan.
- `"0.42"` alone → Rule 2 (sepia from `.42`).
- `"My rating is 0.42 in Mumbai"` → Rule 2. No city+temp pattern (city and number are not paired as temperature; `0.42` is a rating, not °C).

**Why:** The brief explicitly states *"Check these in order, first match wins."* This is deterministic, testable, and avoids subjective heuristics about which pattern is "more important."

**Verified:** `test_rule1_wins_over_decimal` and live API — `"Mumbai 32 and rating 0.42"` returns `ruleApplied: city_temp`.

---

## City + temperature: parse from message (no weather API)

**Decision:** Extract city name and temperature from the user's message text. Do not call an external weather API.

**Why:** The brief says bubble color depends on *"what the user typed"* and describes *"a city and a temperature in Celsius"* in the message — not live weather lookup. A weather API would introduce new ambiguity (typed `32` vs actual `28°C`) and add scope beyond the assignment.

**Verified:** Classifier tests cover `Mumbai 32`, `32C in Berlin`, `it's 20 degrees in Paris`, and negative temps.

---

## Rule 2: sepia ramp (not grayscale)

**Decision:** Use a sepia color ramp for standalone decimals. The brief allows *"Grayscale or sepia"* — sepia was chosen for visual distinction from Rule 1's blue-purple-red spectrum.

**Digit extraction:** Take the first two digits after the decimal point, zero-padded (`.5` → `50` → `0.50`). Map 00–99 to lightness: `.00` lightest, `.99` darkest.

**Verified:** Tests for `3.14`, `0.99`, `.75`, `.5`; live API — `"0.42"` → `ruleApplied: decimal`.

---

## Whole numbers and negative decimals

- `"32"` (integer only) → Rule 3 (LLM panic). Rule 2 requires a decimal point.
- `"-0.5"` → Rule 3. Negative decimals are not in the spec for Rule 2; classifier skips the `-` prefix before the decimal match.

**Verified:** `test_falls_to_panic` for bare `"32"`; `test_negative_decimal_falls_to_panic` for `"-0.5"`.

---

## Rule 1 color mapping (production vs review file)

**Decision:** Implement `temp_to_rgb` in `backend/app/color_engine.py` per brief line 11 — not the buggy `public/review/color_cache.py`.

**Anchors:** deep blue ≤ 0°C, light purple at 15°C, bright red ≥ 35°C, linear interpolation between segments.

**Verified:** `test_fifteen_is_light_purple`, `test_thirty_five_is_bright_red`; live API — `"Mumbai 32"` → `rgb(217, 41, 52)` (32°C in the 15–35°C segment).

---

## Readable text on dynamic backgrounds

**Decision:** Backend computes `textColor` per bubble using relative luminance (`#ffffff` on dark backgrounds, `#000000` on light). Frontend applies the returned color directly on bot bubbles.

**Verified:** Contrast checks across sample temperatures, decimals, and panic scores — all pass.

---

## LLM provider

**Decision:** Groq API with `llama-3.3-70b-versatile` for real conversational replies and Rule 3 panic scoring. `response_format: json_object` for structured bilingual output.

**Verified:** Live API returns non-canned Groq replies on all three rules.

---

## Auth

**Decision:** Email + password with JWT. Backend enforces `@petasight.com` on register, login, `/auth/me`, and `/chat` — not just the login form. Frontend modal validates the domain client-side for faster feedback.

**Verified:** `test_register_rejects_non_petasight` (403), `test_chat_requires_auth` (401).

---

## Bonus: RTL philosopher persona

**Decision:** All LLM replies use **Ibn Sina (Avicenna)** — 11th-century Persian polymath of the Islamic Golden Age — speaking in **Arabic** (RTL script), followed by an English translation. Coloring rules are unchanged; only the reply voice/format is affected.

**Format:** Groq returns JSON `{ "original", "translation" }` (plus `panic_score` for Rule 3). The API `reply` field keeps the combined string for chat history; `meta` carries `persona`, `language`, `original`, and `translation` for the frontend to render RTL block + LTR translation.

**Why Arabic / Ibn Sina:** Arabic is a natural RTL language with a rich tradition of philosophy and science; Ibn Sina fits the brief's "historical philosopher or scientist from that culture." Structured JSON keeps parsing reliable and lets the UI set `dir="rtl"` on the original text without guessing from plain prose.

**Verified:** Live API — all three rules return `meta.persona: "Ibn Sina (Avicenna)"` with Arabic `original` and English `translation`.

---

## Verification summary (against `public/brief.md`)

| Check | Result |
|-------|--------|
| Backend `pytest` (37 tests) | Pass |
| Rule 1 / 2 / 3 classification + colors | Pass |
| First-match ambiguity | Pass |
| `@petasight.com` backend enforcement | Pass |
| Groq LLM (not canned) | Pass |
| Keyboard / contrast accessibility | Pass (manual + luminance tests) |
| `DECISIONS.md`, `REVIEW.md`, `AI_LOG.md` | Present |
| Live deployment + public repo URL | **Live** — [Frontend](https://petasight-chatbot.vercel.app) · [API](https://petasight-chatbot-api.onrender.com) |
