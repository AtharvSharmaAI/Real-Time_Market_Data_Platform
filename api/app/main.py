# OWNER: P3
#
# PURPOSE:
# FastAPI application entry point.
#
# RESPONSIBILITIES:
# Explain:
# - FastAPI application entry point
# - router registration
# - startup/shutdown behavior
#
# DEPENDENCIES:
# fastapi, routers
#
# INTERFACES:
# INPUT: Request
# OUTPUT: Response
#
# IMPLEMENTATION TODO:
# 1. Initialize FastAPI app. 2. Register routers.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.app.config import settings
from api.app.routes.health import router as health_router
from api.app.routes.trades import router as trades_router
from api.app.routes.vwap import router as vwap_router
from api.app.routes.anomalies import router as anomalies_router
from api.app.database import check_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup behavior: verify ClickHouse database connection
    print("Starting up FastAPI application...")
    try:
        if check_connection():
            print("Successfully connected to ClickHouse on startup.")
        else:
            print("Warning: ClickHouse connection could not be established on startup.")
    except Exception as e:
        print(f"Error checking database connection during startup: {e}")
    yield
    # Shutdown behavior
    print("Shutting down FastAPI application...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(trades_router, prefix="/trades", tags=["Trades"])
app.include_router(vwap_router, prefix="/vwap", tags=["VWAP"])
app.include_router(anomalies_router, prefix="/anomalies", tags=["Anomalies"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to the {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app.main:app", host="0.0.0.0", port=8000, reload=False)
