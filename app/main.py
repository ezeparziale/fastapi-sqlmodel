from fastapi import FastAPI

from app.api.api_v1.api import api_router
from fastapi.responses import RedirectResponse
from app.core.config import settings


app = FastAPI()

from app.db.database import engine
from app.models.models import SQLModel
SQLModel.metadata.create_all(engine)


# Routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")