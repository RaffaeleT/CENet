import os
from urllib.parse import quote

from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, get_db
import models
import schemas

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Social Auth"])

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
MICROSOFT_TENANT = os.getenv("MICROSOFT_TENANT", "common")

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

oauth = OAuth()

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="microsoft",
    server_metadata_url=f"https://login.microsoftonline.com/{MICROSOFT_TENANT}/v2.0/.well-known/openid-configuration",
    client_id=MICROSOFT_CLIENT_ID,
    client_secret=MICROSOFT_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="linkedin",
    server_metadata_url="https://www.linkedin.com/oauth/.well-known/openid-configuration",
    client_id=LINKEDIN_CLIENT_ID,
    client_secret=LINKEDIN_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
)


def _get_provider_client(provider: str):
    if provider not in {"google", "microsoft", "linkedin"}:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    return oauth.create_client(provider)


def _extract_user_info(provider: str, token: dict, userinfo: dict | None) -> dict:
    if provider == "google":
        data = userinfo or {}
        return {
            "sub": data.get("sub"),
            "email": data.get("email"),
            "name": data.get("name"),
        }

    if provider == "microsoft":
        data = userinfo or token.get("userinfo") or {}
        return {
            "sub": data.get("sub") or data.get("oid"),
            "email": data.get("email") or data.get("preferred_username"),
            "name": data.get("name"),
        }

    if provider == "linkedin":
        data = userinfo or {}
        return {
            "sub": data.get("sub"),
            "email": data.get("email"),
            "name": data.get("name"),
        }

    raise HTTPException(status_code=400, detail="Unsupported provider")


async def _handle_login(request: Request, provider: str):
    client = _get_provider_client(provider)

    if provider == "google":
        redirect_uri = request.url_for("google_callback")
    elif provider == "microsoft":
        redirect_uri = request.url_for("microsoft_callback")
    elif provider == "linkedin":
        redirect_uri = request.url_for("linkedin_callback")
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    return await client.authorize_redirect(request, redirect_uri)


async def _handle_callback(request: Request, provider: str, db: Session):
    client = _get_provider_client(provider)
    token = await client.authorize_access_token(request)

    userinfo = None
    try:
        userinfo = await client.userinfo(token=token)
    except Exception:
        pass

    social_user = _extract_user_info(provider, token, userinfo)

    email = social_user.get("email")
    provider_sub = social_user.get("sub")
    name = social_user.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="No email returned from provider")

    # Find existing linked account
    user = (
        db.query(models.User)
        .filter(
            models.User.auth_provider == provider,
            models.User.provider_sub == provider_sub
        )
        .first()
    )

    # If no linked account, try by email
    if user is None:
        user = db.query(models.User).filter(models.User.email == email).first()

    # Create new user if still none
    if user is None:
        user = models.User(
            email=email,
            password=None,
            role=None,
            auth_provider=provider,
            provider_sub=provider_sub,
            full_name=name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        changed = False
        if user.auth_provider is None:
            user.auth_provider = provider
            changed = True
        if user.provider_sub is None:
            user.provider_sub = provider_sub
            changed = True
        if name and not user.full_name:
            user.full_name = name
            changed = True
        if changed:
            db.commit()
            db.refresh(user)

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    # frontend reads token, calls /me, and if role is null shows choose-role page
    redirect_target = f"{FRONTEND_URL}/auth/callback?token={quote(access_token)}"
    return RedirectResponse(url=redirect_target)


@router.get("/google/login")
async def google_login(request: Request):
    return await _handle_login(request, "google")


@router.get("/microsoft/login")
async def microsoft_login(request: Request):
    return await _handle_login(request, "microsoft")


@router.get("/linkedin/login")
async def linkedin_login(request: Request):
    return await _handle_login(request, "linkedin")


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    return await _handle_callback(request, "google", db)


@router.get("/microsoft/callback", name="microsoft_callback")
async def microsoft_callback(request: Request, db: Session = Depends(get_db)):
    return await _handle_callback(request, "microsoft", db)


@router.get("/linkedin/callback", name="linkedin_callback")
async def linkedin_callback(request: Request, db: Session = Depends(get_db)):
    return await _handle_callback(request, "linkedin", db)

@router.post("/select-role")
def select_role(
    role_data: schemas.UserRoleSelect,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role has already been selected"
        )

    current_user.role = role_data.role
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Role selected successfully",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
            "full_name": current_user.full_name,
            "auth_provider": current_user.auth_provider
        }
    }