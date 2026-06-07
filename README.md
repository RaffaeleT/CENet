# CENet

Monorepo containing two independently deployable applications:

| App | Folder | Stack |
|-----|--------|-------|
| Frontend | [`frontend/`](frontend/) | Vite + React 19 + TypeScript + Tailwind |
| Backend | [`backend/`](backend/) | FastAPI + SQLAlchemy |

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for how the two apps are wired
together, and [`docs/RESTRUCTURE.md`](docs/RESTRUCTURE.md) for the layout history.

## Running locally

### Backend (port 8000)

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                               # then fill in secrets
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API docs at <http://localhost:8000/docs>.

### Frontend (port 5173)

```bash
cd frontend
npm install
cp .env.example .env                               # set VITE_API_BASE_URL
npm run dev
```

The frontend talks to the backend purely over HTTP using `VITE_API_BASE_URL`;
the backend's CORS allow-list (in `backend/main.py`) must include the frontend's
origin. `localhost:5173` and `localhost:3000` are already allowed.

## Deployment

No deploy config lives in this repo — the backend runs on Render and the frontend
on Vercel, configured in their dashboards. After this restructure, set the
**Render** service root to `backend/` and the **Vercel** project root to
`frontend/`.
