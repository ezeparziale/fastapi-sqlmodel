from fastapi import APIRouter

from app.api.api_v1.endpoints import heros, teams

api_router = APIRouter()

api_router.include_router(heros.router, prefix="/heros", tags=["heros"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
