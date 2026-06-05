from fastapi import APIRouter

router = APIRouter(tags=["Pages"])


@router.get("/home")
def home():
    return {
        "page": "Home",
        "message": "Welcome to CENet Energy HUB"
    }


@router.get("/about")
def about():
    return {
        "page": "About / How it works",
        "message": "CENet connects end users, CER operators, and suppliers in one energy ecosystem."
    }


@router.get("/platform-roles")
def platform_roles():
    return {
        "roles": [
            {
                "name": "user",
                "description": "Households and SMEs using simulations, matching, and REC discovery."
            },
            {
                "name": "operator",
                "description": "CER operators managing communities, incentives, and dashboards."
            },
            {
                "name": "supplier",
                "description": "Suppliers receiving leads and offering services in the platform."
            }
        ]
    }