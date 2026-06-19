from dotenv import load_dotenv

load_dotenv()

import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.auth import get_current_user, router as auth_router
from app.color_engine import decimal_to_rgb, panic_to_rgb, rgb_to_css, temp_to_rgb, text_color_for_bg
from app.database import Base, engine
from app.input_classifier import classify_input, preprocess_message
from app.llm import groq_reply, groq_reply_with_panic
from app.models import User
from app.schemas import ChatRequest, ChatResponse

chat_router = APIRouter(tags=["chat"])


def build_response(reply: str, rgb: tuple[int, int, int], rule: str, meta: dict | None = None) -> ChatResponse:
    return ChatResponse(
        reply=reply,
        backgroundColor=rgb_to_css(rgb),
        textColor=text_color_for_bg(rgb),
        ruleApplied=rule,
        meta=meta,
    )


@chat_router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, user: User = Depends(get_current_user)):
    message = preprocess_message(body.message)
    if not message:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Message cannot be empty")

    history = [{"role": m.role, "content": m.content} for m in body.history]
    rule, meta = classify_input(message)

    if rule == "city_temp":
        rgb = temp_to_rgb(meta["celsius"])
        reply, bilingual = await groq_reply(message, history)
        return build_response(reply, rgb, rule, {**meta, **bilingual})
    if rule == "decimal":
        rgb = decimal_to_rgb(meta["two_digit_value"])
        reply, bilingual = await groq_reply(message, history)
        return build_response(reply, rgb, rule, {**meta, **bilingual})

    reply, panic, bilingual = await groq_reply_with_panic(message, history)
    rgb = panic_to_rgb(panic)
    return build_response(reply, rgb, rule, {"panic_score": panic, **bilingual})


DEFAULT_CORS_ORIGINS = (
    "http://localhost:5173,"
    "http://127.0.0.1:5173,"
    "https://petasight-chatbot.vercel.app"
)


def get_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)
    origins = [o.strip() for o in raw.split(",") if o.strip()]
    if not origins:
        origins = [o.strip() for o in DEFAULT_CORS_ORIGINS.split(",") if o.strip()]
    return origins


def create_app():
    Base.metadata.create_all(bind=engine)

    from fastapi import FastAPI

    app = FastAPI(title="Petasight Chatbot API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_router)
    app.include_router(chat_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
