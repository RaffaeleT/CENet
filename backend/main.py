import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from database import Base, engine, SessionLocal

from auth import router as auth_router
from matching import router as matching_router
from pages import router as pages_router
from simulations import router as simulations_router
from social_auth import router as social_auth_router
from suppliers import router as suppliers_router
from communities import router as communities_router
from event_logs import router as event_logs_router
from reference_data import router as reference_data_router
from admin import router as admin_router
from subscriptions import router as subscriptions_router
from rec_energy import router as rec_energy_router
from personal_energy import router as personal_energy_router
from rec_incentives import router as rec_incentives_router
from newsletter import router as newsletter_router

from logging_utils import log_api_performance

import models


load_dotenv()

app = FastAPI(title="CENet Backend")


@app.middleware("http")
async def log_api_performance_middleware(request: Request, call_next):
    start_time = time.time()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        response_time = round((time.time() - start_time) * 1000, 2)

        ignored_paths = [
            "/",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/favicon.ico",
        ]

        if request.url.path not in ignored_paths:
            db = SessionLocal()

            try:
                log_api_performance(
                    db=db,
                    endpoint=request.url.path,
                    method=request.method,
                    status_code=status_code,
                    response_time=response_time,
                )
            except Exception:
                db.rollback()
            finally:
                db.close()


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET"),
)

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://www.cenet.it",
    "https://cenet.it",
    "https://cenet-frontend.onrender.com",
    "https://fronend-eight-alpha.vercel.app",
    "https://fronend-git-main-laerkevhs-projects.vercel.app",
    # Azure Static Web App (production frontend)
    "https://ambitious-meadow-0a6262703.7.azurestaticapps.net",
]

# Allow an extra origin to be injected via env (e.g. FRONTEND_URL) without a code change.
_frontend_url = os.getenv("FRONTEND_URL")
if _frontend_url and _frontend_url not in allowed_origins:
    allowed_origins.append(_frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(matching_router)
app.include_router(pages_router)
app.include_router(simulations_router)
app.include_router(social_auth_router)
app.include_router(suppliers_router)
app.include_router(communities_router)
app.include_router(event_logs_router)
app.include_router(reference_data_router)
app.include_router(admin_router)
app.include_router(subscriptions_router)
app.include_router(rec_energy_router)
app.include_router(personal_energy_router)
app.include_router(rec_incentives_router)
app.include_router(newsletter_router)


@app.get("/")
def root():
    return {"message": "CENet backend is running"}