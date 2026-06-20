# AI_LOG.md

## Tools I used

- **Cursor** (Agent mode) — main IDE, used for planning, implementation, and debugging
- **Groq API** — LLM powering chat replies and panic scoring (`llama-3.3-70b-versatile`)

---

## Prompts that mattered

**1. Getting the classification logic right before writing any code**

> `analyse the brief then map out all input cases and how to handle each — Rule 1 / Rule 2 / Rule 3 — with examples like "Mumbai 32", "0.99", "HELP ME NOW". Use Groq API for the LLM. Frontend in React JSX, backend in FastAPI.`

I forced it to trace through the full input matrix upfront. That saved a lot of back-and-forth later because the edge cases (decimals that look like temps, city names without temps) were resolved in the plan before any code was written.

**2. Resolving the intentional ambiguity in the spec**

> `The brief leaves one rule underspecified: what happens when a message contains both a city+temperature and a standalone decimal? Pick an answer, build it, explain why in DECISIONS.md. No weather API — parse from what the user typed.`

This is where I made the first-match-wins call. Reasoning is in `DECISIONS.md`.

**3. Tightening the LLM system prompt for the bonus persona**

> `rewrite this system prompt in a much better structured way — use clear sections for Role, Voice, Output format, Guidelines, and Hard constraints`

The original flat paragraph kept making the model drift out of persona within a few turns. Structured sections with explicit hard constraints fixed it.

---

## Where the AI got it wrong

**1. Decimal regex broke on leading-dot values**

The generated pattern `\b(\d*\.\d+)\b` doesn't match `.75` because `\b` doesn't anchor before a dot. I caught this while manually testing Rule 2 inputs. Fixed with a lookaround pattern that handles both `0.75` and `.75` without relying on word boundaries.

**2. Color formula pulled from the wrong file**

Early plan drafts pulled the temperature interpolation logic from `color_cache.py` in the `review/` folder — the file with known bugs. The production `color_engine.py` needed its own correct formula. I caught this during the plan review phase and corrected it explicitly before implementation started.

**3. Negative decimals routing to Rule 2 instead of Rule 3**

`-0.5` was matching the decimal pattern and being colored as Rule 2. The brief doesn't mention negative decimals under Rule 2 and `-0.5` reads as a signed number, not a standalone decimal. Added an explicit check to skip matches preceded by a `-` and fall them through to Rule 3.

**4. CORS config missing the dev origin**

After the initial build, every frontend request returned a 401 or was blocked by CORS. The middleware was rejecting preflight requests before the auth endpoints could respond, and the dev origin wasn't in `CORS_ORIGINS`. Fixed both in one pass.

---

## Hard requirements I verified manually

- **@petasight.com enforcement** — tested that the backend endpoint rejects non-petasight emails directly, not just at the login form. A request with a Gmail address returns 403 at the API level regardless of what the frontend sends.

- **Text readability** — checked contrast across all three color ranges, particularly Rule 3's violet end and Rule 2's dark sepia. Text color switches between dark and light based on background luminance so it stays readable at every point in the ramp.

- **Ambiguous input stress test** — sent `"Mumbai 0.42"` to confirm it routes to Rule 1 and not Rule 2. First-match-wins holds: the city+temp pattern is checked before the decimal pattern, so the city detection wins and the decimal is ignored.