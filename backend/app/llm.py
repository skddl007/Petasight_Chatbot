import json
import os
import re

from groq import Groq

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

PERSONA_NAME = "Ibn Sina (Avicenna)"
PERSONA_LANGUAGE = "ar"
PERSONA_LANGUAGE_LABEL = "Arabic"

PERSONA_SYSTEM = f"""# Role

You are **{PERSONA_NAME}** — the 11th-century Persian polymath, physician, and philosopher of the Islamic Golden Age. You speak with the measured wisdom of someone who has studied medicine, nature, and the soul.

# Voice & language

- Write your reply in **{PERSONA_LANGUAGE_LABEL}**, using proper Arabic script (right-to-left).
- Tone: scholarly, calm, and humane — never cold or preachy.
- You may briefly reference your fields (healing, observation, reason) when it fits naturally.
- Do not break character. Do not mention being an AI or a language model.

# Output format

Return **only** valid JSON — no markdown, no preamble, no trailing commentary.

```json
{{
  "original": "<your Arabic reply>",
  "translation": "<faithful English translation of the Arabic>"
}}
```

# Reply guidelines

1. **Length:** 2–4 sentences in Arabic. Be concise but substantive.
2. **Substance:** Answer what the user actually asked or said. Do not deflect with vague platitudes.
3. **Translation:** The English must faithfully convey the Arabic meaning — same intent, not a paraphrased rewrite.
4. **Script:** `original` must be Arabic text only. `translation` must be English only.

# Hard constraints

- Never omit either field.
- Never wrap the JSON in code fences in your actual response.
- Never reply in English alone — Arabic always comes first in `original`."""

PANIC_SYSTEM_EXTENSION = """# Additional task (panic scoring)

Also assess how **urgent or panicked** the user's latest message sounds.

- `0.0` — completely calm, routine, or reflective
- `0.5` — moderate concern or uncertainty
- `1.0` — extreme panic, crisis, or desperation

Add `panic_score` (a number from 0.0 to 1.0) to your JSON:

```json
{
  "original": "<Arabic reply>",
  "translation": "<English translation>",
  "panic_score": 0.0
}
```"""


_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is required")
        _client = Groq(api_key=api_key)
    return _client


def format_bilingual_reply(original: str, translation: str) -> str:
    return f"{original.strip()}\n\n—\n\n{translation.strip()}"


def parse_bilingual_response(text: str) -> dict[str, str]:
    text = text.strip()
    try:
        data = _parse_json_response(text)
        original = str(data.get("original", "")).strip()
        translation = str(data.get("translation", "")).strip()
        if original and translation:
            return {"original": original, "translation": translation}
        if translation:
            return {"original": original, "translation": translation}
        if original:
            return {"original": original, "translation": original}
    except (json.JSONDecodeError, ValueError, TypeError):
        pass
    return {"original": "", "translation": text or "I'm having trouble responding right now."}


def bilingual_meta(original: str, translation: str) -> dict:
    return {
        "persona": PERSONA_NAME,
        "language": PERSONA_LANGUAGE,
        "original": original,
        "translation": translation,
    }


def _parse_json_response(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise


def _build_messages(message: str, history: list[dict]) -> list[dict]:
    messages = [{"role": "system", "content": PERSONA_SYSTEM}]
    for item in history[-10:]:
        messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": message})
    return messages


async def groq_reply(message: str, history: list[dict]) -> tuple[str, dict]:
    client = _get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=_build_messages(message, history),
        temperature=0.7,
        max_tokens=768,
        response_format={"type": "json_object"},
    )
    text = response.choices[0].message.content or ""
    parsed = parse_bilingual_response(text)
    original = parsed["original"]
    translation = parsed["translation"]
    reply = format_bilingual_reply(original, translation) if original else translation
    return reply, bilingual_meta(original, translation)


async def groq_reply_with_panic(message: str, history: list[dict]) -> tuple[str, float, dict]:
    client = _get_client()
    system = f"{PERSONA_SYSTEM}\n\n{PANIC_SYSTEM_EXTENSION}"
    messages = [{"role": "system", "content": system}]
    for item in history[-10:]:
        messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": message})

    for attempt in range(2):
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=768,
            response_format={"type": "json_object"},
        )
        text = response.choices[0].message.content or ""
        try:
            data = _parse_json_response(text)
            original = str(data.get("original", "")).strip()
            translation = str(data.get("translation", "")).strip()
            panic_score = float(data.get("panic_score", 0.5))
            panic_score = max(0.0, min(1.0, panic_score))

            if not translation and not original:
                raise ValueError("empty reply")

            if not translation:
                translation = original
            if not original:
                original = translation

            reply = format_bilingual_reply(original, translation)
            meta = bilingual_meta(original, translation)
            return reply, panic_score, meta
        except (json.JSONDecodeError, ValueError, TypeError):
            if attempt == 1:
                fallback = parse_bilingual_response(text)
                original = fallback["original"]
                translation = fallback["translation"]
                reply = format_bilingual_reply(original, translation) if original else translation
                return reply, 0.5, bilingual_meta(original, translation)

    fallback = "I'm having trouble responding right now."
    return fallback, 0.5, bilingual_meta("", fallback)
