# apps/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.routers import analyze, health

app = FastAPI(title="Agno Finance Agents", version="1.0")

# Allow the Django UI origins
origins = [
    "http://127.0.0.1:9000",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/v1")
app.include_router(analyze.router, prefix="/v1")
