# SvelteKit 5 + FastAPI Starter

A production-ready starter template combining **SvelteKit 5** with **FastAPI**, featuring JWT authentication, a dark theme, and Docker deployment.

Built and maintained by [Darren Betney](https://github.com/Quartalis).

---

## What's Included

- SvelteKit 5 frontend (TypeScript)
- FastAPI backend
- JWT login & registration
- Dark theme (Tailwind v4)
- Docker Compose deployment

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
├── backend/
│   ├── main.py              # FastAPI app with auth endpoints
│   ├── config.py            # Environment-based configuration
│   ├── requirements.txt     # Python dependencies
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
