# Petasight Chatbot

Full-stack chatbot take-home: bubble background color depends on what the user typed. React (JSX) frontend + FastAPI backend + Groq LLM.

## Live demo

| | URL |
|---|-----|
| **Frontend** | https://petasight-chatbot.vercel.app |
| **Backend API** | https://petasight-chatbot-api.onrender.com |
| **Health check** | https://petasight-chatbot-api.onrender.com/health |

## Features

- **Rule 1:** City + temperature → blue/purple/red gradient
- **Rule 2:** Standalone decimal → sepia ramp (`.00` lightest, `.99` darkest)
- **Rule 3:** Everything else → Groq panic score → violet/magenta/pale yellow
- **Auth:** Email/password, `@petasight.com` only (enforced on backend)
- **Accessibility:** Keyboard navigation, readable text on dynamic backgrounds
- **Bonus:** Replies in Arabic as Ibn Sina (Avicenna), original script (RTL) then English translation

## Quick start (local)

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set GROQ_API_KEY and JWT_SECRET
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173

### Tests

```bash
cd backend
pytest   # 37 tests — classifier, colors, auth, LLM helpers
```

## Environment variables

| Variable | Where | Description |
|----------|-------|-------------|
| `GROQ_API_KEY` | Render | Groq API key |
| `JWT_SECRET` | Render | JWT signing secret |
| `DATABASE_URL` | Render | SQLite or Postgres URL |
| `CORS_ORIGINS` | Render | `https://petasight-chatbot.vercel.app` |
| `VITE_API_URL` | Vercel | `https://petasight-chatbot-api.onrender.com` |

## Deployment

**Backend → Render** · **Frontend → Vercel**

Full guide: **[DEPLOY.md](DEPLOY.md)**

## Deliverables

- [`DEPLOY.md`](DEPLOY.md) — Render + Vercel deployment guide
- [`DECISIONS.md`](DECISIONS.md) — ambiguity resolution and design choices
- [`REVIEW.md`](REVIEW.md) — bugs in `public/review/color_cache.py`
- [`AI_LOG.md`](AI_LOG.md) — AI tools and corrections

##   API

```
POST /auth/register  { email, password }
POST /auth/login     { email, password }  → { access_token }
GET  /auth/me        Authorization: Bearer <token>
POST /chat           { message, history? }  → { reply, backgroundColor, textColor, ruleApplied, meta? }
```

`meta` includes bilingual fields when the bonus persona is active: `persona`, `language`, `original`, `translation` (and `panic_score` for Rule 3).
