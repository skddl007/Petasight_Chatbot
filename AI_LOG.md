# AI_LOG.md

## Tools used

- **Cursor** (Agent mode) — primary IDE and implementation assistant
- **Groq API** — LLM for chat replies and panic scoring (`llama-3.3-70b-versatile`)

## Prompts that mattered

1. *"Implement the full-stack chatbot plan: React JSX frontend, FastAPI backend, three-tier bubble coloring, @petasight.com auth, Groq LLM."*
2. *"All input cases matrix — Rule 1 city+temp without requiring °C, Rule 2 decimals only, Rule 3 panic, first match wins."*
3. *"Color mapping per brief.md lines 11–13, not the buggy color_cache.py review file."*
4. *"Bonus: RTL language, historical philosopher/scientist voice, original script then English translation."*
5. *"Verify everything against brief.md — run tests and live API checks."*

## Where the AI got it wrong (and fixes)

1. **Decimal regex for `.75` and `.5`:** Initial pattern `\b(\d*\.\d+)\b` failed on leading-dot decimals like `.75`. Fixed with `(?:^|(?<!\d))(\.\d+|\d+\.\d+)(?!\d)`.

2. **Negative decimals:** Pattern matched `0.5` inside `-0.5`. Fixed by checking for a `-` character immediately before the match and skipping.

3. **Color cache bug framing:** Early plan referenced "fix bug from color_cache.py" for production code. Corrected: brief.md is the source of truth; color_cache.py bugs belong only in REVIEW.md. Production `color_engine.py` uses correct `(celsius - 15) / 20.0` interpolation — confirmed by `test_fifteen_is_light_purple`.

4. **PowerShell command chaining:** Used `&&` in shell commands on Windows PowerShell — failed. Switched to `;` separator.

5. **Ambiguity example `"My rating is 0.42 in Mumbai"`:** Initially flagged as Rule 2 only because city and number aren't adjacent. Confirmed correct after review — `0.42` is a rating, not Celsius; loosening Rule 1 would mis-color non-weather messages.

6. **LLM system prompt:** First persona prompt was flat and easy for the model to ignore. Rewrote with structured sections (Role, Voice, Output format, Guidelines, Hard constraints) plus a separate panic-scoring extension for Rule 3.

## Judgment calls made

- Parse city+temp from message (no weather API) — see DECISIONS.md
- First match wins for city+temp vs decimal ambiguity
- Sepia ramp for Rule 2 decimals
- Email/password auth with backend domain enforcement on all protected routes
- Ibn Sina / Arabic for bonus persona; JSON `original` + `translation` for reliable RTL rendering
- Login/register as modal popups over a landing page (UX polish, not required by brief)

## Self-check (verification run)

Ran against `public/brief.md` requirements:

- **37/37** backend tests pass (`pytest`)
- **Live API** on `localhost:8000`: auth rejection, all three color rules, ambiguity case `"Mumbai 32 and rating 0.42"` → Rule 1, bilingual meta on every reply
- **Contrast:** luminance-based text color passes across sample Rule 1/2/3 backgrounds
- **Frontend:** `npm run build` succeeds
- **Still outstanding before submission:** deploy to Vercel + backend host, push public repo, add live URLs to README
