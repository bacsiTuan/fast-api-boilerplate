from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

# from fast_api_app.api_v1.api import api_router
from app.config import settings
from fast_api_app.api_v1 import login

app = FastAPI(
    title="FastAPI", openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])

app.include_router(api_router, prefix=settings.API_V1_STR)
