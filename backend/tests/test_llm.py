from app.llm import format_bilingual_reply, parse_bilingual_response


def test_format_bilingual_reply():
    result = format_bilingual_reply("مرحبا", "Hello")
    assert result == "مرحبا\n\n—\n\nHello"


def test_parse_bilingual_response_json():
    text = '{"original": "السلام", "translation": "Peace"}'
    parsed = parse_bilingual_response(text)
    assert parsed["original"] == "السلام"
    assert parsed["translation"] == "Peace"


def test_parse_bilingual_response_fallback():
    parsed = parse_bilingual_response("Plain English fallback")
    assert parsed["translation"] == "Plain English fallback"
    assert parsed["original"] == ""
