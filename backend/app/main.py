from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import content, categorize, analytics
from .core.config import settings

app = FastAPI(title="AI Content Manager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(categorize.router,
                   prefix="/api/v1/categorize", tags=["categorize"])
app.include_router(
    analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
