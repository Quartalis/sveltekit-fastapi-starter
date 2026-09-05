# SvelteKit 5 + FastAPI Starter

[![CI](https://github.com/Quartalis/sveltekit-fastapi-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/Quartalis/sveltekit-fastapi-starter/actions/workflows/ci.yml)

A production-ready starter template combining **SvelteKit 5** with **FastAPI**, featuring JWT authentication, a dark theme, and Docker deployment.

Built and maintained by [Darren Betney](https://github.com/Quartalis).

---

## What's Included

- SvelteKit 5 frontend (TypeScript)
- FastAPI backend
- JWT login & registration
- Dark theme (Tailwind v4)
- Docker Compose deployment
- Backend test suite (pytest) + GitHub Actions CI

---

## Quick Start

### With Docker (recommended)

```bash
git clone https://github.com/Quartalis/sveltekit-fastapi-starter.git
cd sveltekit-fastapi-starter
cp .env.example .env
# Edit .env and set a real JWT_SECRET
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

### Without Docker

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
sveltekit-fastapi-starter/
├── .github/workflows/
│   └── ci.yml               # Backend tests, frontend check+build, Docker builds
├── backend/
│   ├── main.py              # FastAPI app with auth endpoints
│   ├── config.py            # Environment-based configuration
│   ├── tests/
│   │   ├── conftest.py      # TestClient + clean user store per test
│   │   └── test_api.py      # Health, register, login, /api/me, token edge cases
│   ├── requirements.txt     # Python dependencies
│   ├── requirements-dev.txt # + pytest, httpx
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api.ts       # API client
│   │   │   └── auth.ts      # Auth store
│   │   └── routes/
│   │       ├── +layout.svelte
│   │       ├── +page.svelte
│   │       ├── login/
│   │       ├── register/
│   │       └── dashboard/
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── LICENSE
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/health` | Health check | No |
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login (returns JWT) | No |
| GET | `/api/me` | Get current user | Yes |

---

## Tests & CI

**Backend** (15 tests: health, registration incl. duplicate/invalid input, login success/failure, `/api/me` with valid, missing, garbage, wrong-secret, expired and orphaned tokens):

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest -v tests
```

**Frontend** (type-check + production build):

```bash
cd frontend
npm ci
npm run check
npm run build
```

GitHub Actions (`.github/workflows/ci.yml`) runs all of the above on every push and pull request — backend on Python 3.11 and 3.12, frontend on Node 20 — then builds both Docker images once those pass.

---

## Tech Stack

- **Frontend:** SvelteKit 5, Tailwind CSS v4, TypeScript
- **Backend:** FastAPI, Pydantic v2, python-jose, passlib
- **Infrastructure:** Docker, Docker Compose

---

## Configuration

All configuration is done via environment variables. See `.env.example` for available options.

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_SECRET` | `change-me-in-production` | Secret key for JWT signing |
| `JWT_EXPIRY_HOURS` | `24` | Token expiry time |
| `CORS_ORIGINS` | `http://localhost:5173,...` | Allowed CORS origins |

---

## License

MIT License. See [LICENSE](LICENSE) for details.
