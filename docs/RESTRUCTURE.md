# CENet — Repository Restructure (executed)

> **Status: done** (not yet committed). This records the restructure that split
> the two apps into clean sibling folders. See [ARCHITECTURE.md](ARCHITECTURE.md)
> for the resulting layout.

## Why

The git root was a folder named `backend` that actually held the **frontend** at
its top level, with the **Python backend** nested inside it as `Backend/` (capital
B). This `backend/` ⊃ `Backend/` collision was confusing and obscured that these
are two independently deployable apps.

## What changed

```
frontend/   <- all the Vite/React files that used to sit at the repo root
backend/    <- the contents of the old Backend/ folder (lowercase, un-nested)
docs/       <- unchanged
README.md   <- new: how to run both apps
.gitignore  <- consolidated; build/cache artifacts now ignored
```

### Steps performed

1. **Untracked build/cache artifacts** (kept on disk, removed from git index):
   `node_modules/`, `dist/`, `.vite/`, the root `__pycache__/`, and `.DS_Store`.
2. **`git mv` (history-preserving)**:
   - root frontend files (`src/`, `public/`, `index.html`, `vite.config.ts`,
     `eslint.config.js`, `postcss.config.js`, `package.json`, `package-lock.json`,
     `tsconfig*.json`) → `frontend/`
   - `Backend/` → `backend/` (via a temp name, since the rename is case-only on a
     case-insensitive filesystem).
3. **Consolidated root `.gitignore`** (frontend node_modules/dist/.vite, backend
   __pycache__/pyc/venv/test.db, secrets) and fixed its malformed trailing line.
4. **Removed the dead duplicate route**: `public_roi.py` was **byte-identical** to
   `personal_energy.py` (same `/personal-energy` prefix and same paths), so its
   routes were shadowed and never reached. Deleted the file and removed its import
   + `include_router` in `backend/main.py`. The `simulation_type` value
   `"public_roi"` in `models.py` is unrelated and was left as-is.
5. **Added** `frontend/.env.example`, `backend/.env.example`, and `README.md`.

### Deviation from the original plan

The plan proposed moving the **git root up to `CENet/`**. That was **not done**:
the working directory and IDE session are rooted at the current repo
(`…/CENet/backend`), and relocating `.git` would break them. Instead the split was
done **in place** — the repo root stays where it is and now contains `frontend/`
and `backend/` as siblings. The repo's physical top-level folder is still named
`backend`; it can be renamed at the OS level later as a separate, low-risk step
(close the IDE, rename the folder, reopen).

## Required manual follow-up (out-of-repo)

No deploy config lives in the repo, so update the dashboards:

- **Render** (backend): set service root/working dir to `backend/`, start command
  `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- **Vercel** (frontend): set project root to `frontend/`, build `npm run build`,
  output `dist`, and set `VITE_API_BASE_URL`.

## Verification

- `git status` shows renames (R) rather than add/delete pairs → history preserved.
- `git ls-files | grep node_modules` returns nothing.
- Top-level tracked entries: `frontend/`, `backend/`, `docs/`, `README.md`,
  `.gitignore`, `.vscode/`.
- `backend/main.py` parses and no longer imports `public_roi`.
- **Still to do by a human** (needs deps + a DB): start the backend from
  `backend/` (`uvicorn main:app`), start the frontend from `frontend/`
  (`npm run dev` with `VITE_API_BASE_URL=http://localhost:8000`), and confirm a
  login round-trip + `/personal-energy/*` endpoints work.
