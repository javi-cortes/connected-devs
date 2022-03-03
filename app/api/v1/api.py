from fastapi import APIRouter

from app.api.v1.endpoints import connected

api_router = APIRouter()
api_router.include_router(connected.router, prefix="/connected", tags=["connected"])

tags_metadata = [
    {
        "name": "connected",
        "description": """Will return whether two 
        developers are fully check_connection_between or not. Given a pair of developer
        handles they are considered check_connection_between if:
            ● They follow each other on Twitter.
            ● They have at least a Github organization in common.",
        """,
    },
]
