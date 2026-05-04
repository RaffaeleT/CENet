from fastapi import APIRouter

router = APIRouter(prefix="/reference", tags=["Reference Data"])


@router.get("/regions")
def get_regions():
    return {
        "regions": [
            "Abruzzo",
            "Basilicata",
            "Calabria",
            "Campania",
            "Emilia-Romagna",
            "Friuli-Venezia Giulia",
            "Lazio",
            "Liguria",
            "Lombardia",
            "Marche",
            "Molise",
            "Piemonte",
            "Puglia",
            "Sardegna",
            "Sicilia",
            "Toscana",
            "Trentino-Alto Adige",
            "Umbria",
            "Valle d'Aosta",
            "Veneto"
        ]
    }


@router.get("/provinces")
def get_provinces():
    return {
        "provinces": [
            {"name": "Milano", "region": "Lombardia"},
            {"name": "Roma", "region": "Lazio"},
            {"name": "Torino", "region": "Piemonte"},
            {"name": "Napoli", "region": "Campania"},
            {"name": "Bologna", "region": "Emilia-Romagna"},
            {"name": "Firenze", "region": "Toscana"},
            {"name": "Venezia", "region": "Veneto"},
            {"name": "Palermo", "region": "Sicilia"},
            {"name": "Bari", "region": "Puglia"},
            {"name": "Cagliari", "region": "Sardegna"}
        ]
    }


@router.get("/community-statuses")
def get_community_statuses():
    return {
        "statuses": [
            "draft",
            "forming",
            "active",
            "paused",
            "closed"
        ]
    }


@router.get("/need-types")
def get_need_types():
    return {
        "need_types": [
            "join_rec",
            "create_rec",
            "pv_installation",
            "battery_storage",
            "energy_audit",
            "consulting",
            "financing"
        ]
    }


@router.get("/supplier-categories")
def get_supplier_categories():
    return {
        "categories": [
            "audit",
            "pv",
            "bess",
            "cer_support",
            "consulting"
        ]
    }


@router.get("/roles")
def get_roles():
    return {
        "roles": [
            {
                "value": "user",
                "label": "User",
                "description": "Households and SMEs using simulations and matching."
            },
            {
                "value": "operator",
                "label": "CER Manager",
                "description": "Community managers managing Renewable Energy Communities."
            },
            {
                "value": "supplier",
                "label": "Supplier",
                "description": "Service providers receiving leads and offering energy services."
            }
        ]
    }