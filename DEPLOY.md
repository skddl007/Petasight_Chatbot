# Deployment Guide

Deploy **backend on Render** and **frontend on Vercel**. Order matters: deploy the backend first so you have the API URL for the frontend.

## Prerequisites

- GitHub repo with this project pushed (public or private)
- [Groq API key](https://console.groq.com/)
- [Render](https://render.com/) account (free tier works)
- [Vercel](https://vercel.com/) account (free tier works)

---

## 1. Backend — Render

### Option A: Blueprint (recommended)

1. Push the repo to GitHub.
2. In Render → **New** → **Blueprint**.
3. Connect the repo — Render reads [`render.yaml`](render.yaml) at the repo root.
4. Set **GROQ_API_KEY** when prompted (secret).
5. Leave **CORS_ORIGINS** empty for now; add it after Vercel deploy (step 2).
6. Click **Apply** and wait for the build (~5–10 min on free tier).

### Option B: Manual web service

1. Render → **New** → **Web Service** → connect repo.
2. Settings:
   | Field | Value |
   |-------|--------|
   | **Root Directory** | *(leave empty — repo root)* |
   | **Runtime** | Docker |
   | **Dockerfile Path** | `backend/Dockerfile` |
   | **Docker Context** | `backend` |
   | **Health Check Path** | `/health` |
3. Environment variables:

   | Key | Value |
   |-----|--------|
   | `GROQ_API_KEY` | your Groq key |
   | `JWT_SECRET` | long random string |
   | `GROQ_MODEL` | `llama-3.3-70b-versatile` |
   | `DATABASE_URL` | `sqlite:///./chatbot.db` |
   | `CORS_ORIGINS` | *(set after Vercel — step 2b)* |

4. **Create Web Service**.

### Verify backend

Your API URL will look like:

`https://petasight-chatbot-api.onrender.com`

Test:

```bash
curl https://YOUR-RENDER-URL.onrender.com/health
# → {"status":"ok"}
```

> **Note:** Free Render services spin down after inactivity. First request may take ~30s (cold start).

> **Database:** Default SQLite works for the demo. User accounts reset on redeploy. For persistence, add a [Render Postgres](https://render.com/docs/databases) instance and set `DATABASE_URL` to the Postgres connection string.

---

## 2. Frontend — Vercel

1. Vercel → **Add New** → **Project** → import the same GitHub repo.
2. Configure:

   | Field | Value |
   |-------|--------|
   | **Framework Preset** | Vite |
   | **Root Directory** | `frontend` |
   | **Build Command** | `npm run build` |
   | **Output Directory** | `dist` |

3. Environment variables:

   | Key | Value |
   |-----|--------|
   | `VITE_API_URL` | `https://YOUR-RENDER-URL.onrender.com` |

4. **Deploy**.

Your frontend URL will look like:

`https://your-project.vercel.app`

### 2b. Connect backend CORS

Back in **Render** → your web service → **Environment**:

| Key | Value |
|-----|--------|
| `CORS_ORIGINS` | `https://your-project.vercel.app` |

No trailing slash. Redeploy or save — Render restarts automatically.

If you use a custom Vercel domain, include that URL too (comma-separated):

```
https://your-project.vercel.app,https://www.yourdomain.com
```

---

## 3. Smoke test (production)

1. Open the Vercel URL.
2. **Register** with `you@petasight.com` / password (min 6 chars).
3. Send:
   - `Mumbai 32` → red-ish bubble (Rule 1)
   - `0.42` → sepia bubble (Rule 2)
   - `HELP ME NOW` → violet bubble (Rule 3)
4. Confirm Arabic + English reply (bonus persona).

---

## Environment variable cheat sheet

| Variable | Service | Example |
|----------|---------|---------|
| `GROQ_API_KEY` | Render | `gsk_...` |
| `JWT_SECRET` | Render | random 32+ char string |
| `CORS_ORIGINS` | Render | `https://app.vercel.app` |
| `DATABASE_URL` | Render | `sqlite:///./chatbot.db` or Postgres URL |
| `VITE_API_URL` | Vercel | `https://api.onrender.com` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Frontend can't reach API | Check `VITE_API_URL` on Vercel; rebuild after changing it |
| CORS error in browser | Set `CORS_ORIGINS` on Render to exact Vercel URL (https, no slash) |
| 502 / timeout on first chat | Render cold start — wait and retry |
| `GROQ_API_KEY` error | Set key on Render and redeploy |
| Registration works locally but not prod | Re-register after deploy (SQLite resets on Render redeploy) |

---

## Files used for deployment

| File | Purpose |
|------|---------|
| [`render.yaml`](render.yaml) | Render Blueprint (backend) |
| [`backend/Dockerfile`](backend/Dockerfile) | FastAPI + uvicorn container |
| [`frontend/vercel.json`](frontend/vercel.json) | SPA rewrites for Vercel |
