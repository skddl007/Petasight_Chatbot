# Full-Stack Engineer Take-Home

Plan for about 90 minutes. Use the AI tools you actually code with (Cursor, Claude Code, Copilot, v0). We assume the AI writes most of the code, so that isn't what we're grading. We're reading for the judgment on top of it: where you caught it being wrong, what you did when the spec was fuzzy, and whether you checked your own work.

Send a short `AI_LOG.md` with the code: the tools you used, the few prompts that mattered, and a couple of places the AI got it wrong that you had to fix. We score the submission on its own, with no call, so let your writeups (this one, plus `DECISIONS.md` and `REVIEW.md` below) carry the weight.

## What to build

A chatbot, deployed on Vercel (or anywhere with a live URL), plus a public repo. The background color of each reply bubble depends on what the user typed. Check these in order, first match wins:

1. A city and a temperature in Celsius. Color between deep blue and bright red by temperature: deep blue at 0 or below, light purple around 15, bright red at 35 or above.
2. Otherwise, a standalone decimal number. Grayscale or sepia ramp from the first two decimal digits: .00 lightest, .99 darkest.
3. Otherwise, ask the LLM how urgent or panicked the message sounds, and color it from violet for high panic, through magenta, to pale yellow for completely calm.

Hard requirements:

- A real LLM on the backend, not canned replies. You can shut the project off a week after you send it.
- It works with a keyboard, and the text stays readable as the background color shifts. We care about this one, and we'll open the app and check it ourselves.
- Only `@petasight.com` emails get in. The backend endpoint must enforce this rule, not just the login page.

## The part we actually read for

- One rule above is underspecified on purpose: what happens when a message has both a city-and-temperature and a standalone decimal? Don't email us to ask. Pick an answer, build it, and say why in a `DECISIONS.md`.
- The `review/` folder has a small module and its test with a few bugs. Tell us what's broken, why, and how you'd fix it, in a `REVIEW.md`.

That's the whole thing. We're reading for your judgment, how you handle the ambiguous bit, how you read someone else's code, and whether you tested your own work. Not how many features you packed in.

(Bonus, only if you're enjoying it: have the bot reply in a right-to-left language, in the voice of a historical philosopher or scientist from that culture, original script then an English translation.)
