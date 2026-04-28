import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from database import Base, engine
from auth import router as auth_router
from matching import router as matching_router
from pages import router as pages_router
from simulations import router as simulations_router
from social_auth import router as social_auth_router
from suppliers import router as suppliers_router
import models

load_dotenv()

app = FastAPI(title="CENet Backend")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "fallback-secret")
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(matching_router)
app.include_router(pages_router)
app.include_router(simulations_router)
app.include_router(social_auth_router)
app.include_router(suppliers_router)


@app.get("/")
def root():
    return {"message": "CENet backend is running"}