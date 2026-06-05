# CENet — Architecture & Wiring

> How the two applications in this repository fit together.

## 1. Overview — one repo, two apps

This repository is a monorepo with **two independently deployable applications**
as sibling folders:

- [`frontend/`](../frontend/) — a Vite + React 19 + TypeScript app
  (`package.json` → `"tailadmin-react"`).
- [`backend/`](../backend/) — a FastAPI service (Python).

> **History note:** the repo was previously laid out with the frontend at the git
> root and the backend nested in a `Backend/` subfolder. It was restructured into
> the clean split above — see [RESTRUCTURE.md](RESTRUCTURE.md). The repository's
> top-level folder is still physically named `backend`; that's the git root, and
> it contains the `frontend/` and `backend/` siblings.

## 2. Component map

```
<repo root>/
├── README.md
├── .gitignore                     <- consolidated; build artifacts now ignored
├── docs/                          <- ARCHITECTURE.md, RESTRUCTURE.md
├── frontend/                      <- Vite + React 19 + TS
│   ├── package.json  vite.config.ts  index.html  tsconfig*.json
│   ├── .env.example               <- VITE_API_BASE_URL
│   ├── public/
│   └── src/
│       ├── App.tsx                <- react-router v7 route table
│       ├── main.tsx               <- entry; ThemeProvider + Helmet
│       ├── components/
│       │   ├── services/          <- fetch-based API client (auth, communities, roi, sme)
│       │   ├── auth/              <- SignInForm, SignUpForm (+ OAuth buttons)
│       │   ├── ui/ form/ common/ header/ charts/ …
│       ├── context/               <- ThemeContext, SidebarContext
│       ├── layout/                <- AppLayout, AppHeader, AppSidebar
│       └── pages/                 <- route-level pages (per-role dashboards, simulators)
└── backend/                       <- FastAPI service
    ├── main.py                    <- app factory, middleware, router includes
    ├── database.py                <- SQLAlchemy engine/session, DATABASE_URL
    ├── models.py  schemas.py      <- ORM models / Pydantic schemas
    ├── auth.py  social_auth.py    <- JWT auth + OAuth (Google/Microsoft/LinkedIn)
    ├── admin.py communities.py matching.py subscriptions.py newsletter.py
    │   personal_energy.py rec_energy.py rec_incentives.py simulations.py
    │   suppliers.py pages.py reference_data.py event_logs.py
    ├── logging_utils.py
    ├── requirements.txt
    └── .env.example               <- DATABASE_URL, SECRET_KEY, SESSION_SECRET, …
```

## 3. Frontend

- **Stack**: Vite 6, React 19, TypeScript 5.7, Tailwind CSS 4, react-router 7.
  No HTTP-client library and no global state library.
- **API layer**: plain `fetch()` calls grouped in
  [frontend/src/components/services/](../frontend/src/components/services/)
  (`auth.ts`, `communities.ts`, `roi.ts`, `sme.ts`). Base URL comes from
  `import.meta.env.VITE_API_BASE_URL` (the **only** frontend env var).
- **Routing** ([frontend/src/App.tsx](../frontend/src/App.tsx)): `/signin` and
  `/signup` render outside the layout; everything else renders inside `AppLayout`
  (`/`, `/dashboard`, `/admin-dashboard`, `/cer-manager`, `/supplier-dashboard`,
  `/roi-simulator`, `/sme-optimizer`, `/matching`, `/services`, `/profile`), with
  `*` → NotFound.
- **Auth state**: JWT kept in `localStorage` under key `"token"`; sent as
  `Authorization: Bearer <token>`. After login the app calls `/me`, reads the
  role, and redirects (admin → `/admin-dashboard`, operator → `/cer-manager`,
  supplier → `/supplier-dashboard`, else → `/dashboard`).
- **Contexts**: `ThemeContext` (dark/light, persisted to `localStorage`) and
  `SidebarContext` (UI only).
- **Dev server**: default Vite port `5173`. **No proxy** to the backend — the
  browser calls the backend directly, so CORS (below) is what couples them.

## 4. Backend

- **App**: `FastAPI(title="CENet Backend")` in
  [backend/main.py](../backend/main.py). `load_dotenv()` runs first;
  `Base.metadata.create_all(bind=engine)` creates tables on startup.
- **Imports are flat** (`from auth import …`) — run **from inside `backend/`**:
  `uvicorn main:app --host 0.0.0.0 --port 8000`.
- **Middleware** (in order): a custom `http` middleware logging API performance to
  `APIPerformanceLog` (skips `/`, `/docs`, `/openapi.json`, `/redoc`,
  `/favicon.ico`); `SessionMiddleware` (`SESSION_SECRET`); `CORSMiddleware` (§5).
- **Routers** — 15 included in [backend/main.py](../backend/main.py):

  | Router file | Prefix | Notes |
  |---|---|---|
  | `auth.py` | _(none)_ | `/register`, `/login`, `/me` |
  | `social_auth.py` | `/auth` | Google / Microsoft / LinkedIn OAuth |
  | `pages.py` | _(none)_ | `/home`, `/about`, `/platform-roles` |
  | `matching.py` | `/matching` | |
  | `communities.py` | `/communities` | |
  | `suppliers.py` | `/suppliers` | |
  | `simulations.py` | `/simulations` | `/roi`, `/sme`, … |
  | `subscriptions.py` | `/subscriptions` | |
  | `newsletter.py` | `/newsletter` | |
  | `reference_data.py` | `/reference` | regions, provinces, roles, … |
  | `event_logs.py` | `/event-logs` | |
  | `admin.py` | `/admin` | dashboard, users, events, errors, performance |
  | `rec_energy.py` | `/rec-energy` | |
  | `rec_incentives.py` | `/rec-incentives` | |
  | `personal_energy.py` | `/personal-energy` | `/upload`, `/manual`, `/uploads`, `/kpis` |

- **Database**: SQLAlchemy 2.0. `DATABASE_URL` from env, default
  `sqlite:///./test.db`; `postgres://`→`postgresql://` rewrite present;
  `psycopg2-binary` in requirements implies Postgres/Neon/Azure in production.

## 5. How the two apps communicate

There is **no shared code and no dev proxy** between the apps. They are coupled by
exactly two things: the frontend's `VITE_API_BASE_URL` and the backend's CORS
allow-list.

**CORS allow-list** (in [backend/main.py](../backend/main.py),
`allow_credentials=True`, `allow_methods=["*"]`, `allow_headers=["*"]`):

```
http://localhost:3000  :5173  :5174   (and 127.0.0.1 equivalents)
https://www.cenet.it    https://cenet.it
https://cenet-frontend.onrender.com
https://fronend-eight-alpha.vercel.app
https://fronend-git-main-laerkevhs-projects.vercel.app
```

**Login round-trip:**

```
Browser (React)                         FastAPI (backend/)
   │  POST /login (form-urlencoded)        │
   │ ─────────────────────────────────────▶│  auth.py: verify bcrypt, sign JWT
   │  { access_token, token_type }         │
   │ ◀─────────────────────────────────────│
   │  localStorage["token"] = access_token │
   │                                        │
   │  GET /me  Authorization: Bearer <jwt>  │
   │ ─────────────────────────────────────▶│  get_current_user() decodes JWT
   │  { id, email, role, full_name, … }     │
   │ ◀─────────────────────────────────────│
   │  redirect by role                      │
   ▼                                        ▼
(every later API call carries the same Bearer header; CORS gates the origin)
```

## 6. Authentication deep-dive

- **Local**: `POST /register`, `POST /login` (OAuth2 password grant). JWT is
  HS256, 60-min expiry, signed with `SECRET_KEY`
  ([backend/auth.py](../backend/auth.py)). Passwords hashed with bcrypt
  (passlib). `get_current_user()` guards protected routes; `require_role([...])`
  enforces RBAC.
- **Bootstrap admin**: `auth.py` contains a hardcoded admin
  (`admin@gmail.com` / `Admin!1234`) that creates/updates an `admin@cenet.local`
  user with the admin role. ⚠️ Move to env/seed before production.
- **OAuth** ([backend/social_auth.py](../backend/social_auth.py), prefix
  `/auth`): Google, Microsoft (`MICROSOFT_TENANT`, default `common`), LinkedIn.
  Callbacks create/link a user by email, issue a JWT, and redirect to
  `FRONTEND_URL` with the token in the query string. `POST /auth/select-role`
  lets social signups pick a role.

## 7. Configuration / environment variables

**Frontend** ([frontend/.env.example](../frontend/.env.example)):

| Var | Purpose | Default |
|---|---|---|
| `VITE_API_BASE_URL` | Backend base URL for all `fetch` calls | _(none — must be set)_ |

**Backend** ([backend/.env.example](../backend/.env.example), via `python-dotenv`):

| Var | Purpose | Default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./test.db` |
| `SECRET_KEY` | JWT signing secret | _(required)_ |
| `SESSION_SECRET` | SessionMiddleware secret | _(required)_ |
| `FRONTEND_URL` | OAuth callback redirect target | `http://localhost:3000` |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Google OAuth | _(optional)_ |
| `MICROSOFT_CLIENT_ID` / `MICROSOFT_CLIENT_SECRET` | Microsoft OAuth | _(optional)_ |
| `MICROSOFT_TENANT` | Microsoft tenant | `common` |
| `LINKEDIN_CLIENT_ID` / `LINKEDIN_CLIENT_SECRET` | LinkedIn OAuth | _(optional)_ |

## 8. Known issues / notes

- **Bootstrap admin is hardcoded** in `auth.py` (`admin@gmail.com` /
  `Admin!1234`) — move to env/seed before production.
- **JWT in `localStorage`** — convenient but XSS-exposed; consider the tradeoff
  for production.
- **No in-repo deploy config** — deploys are configured in the Render/Vercel
  dashboards. After the restructure, the Render service root is `backend/` and the
  Vercel project root is `frontend/`.

> Two issues documented in earlier versions of this file are now **resolved**:
> the duplicate/shadowed `public_roi.py` router (identical to `personal_energy.py`)
> was removed, and the committed build artifacts (`node_modules/`, `dist/`,
> `.vite/`, `__pycache__/`) are now untracked and `.gitignore`'d. See
> [RESTRUCTURE.md](RESTRUCTURE.md).
