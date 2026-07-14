from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .core.logging import configure_logging, get_logger
from .api.v1 import health, auth, documents, chat

configure_logging()
logger = get_logger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

print("\n========== REGISTERED ROUTES ==========")
for route in app.routes:
    print(route.path, route.methods)
print("=======================================\n")
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application", app_name=settings.APP_NAME, version=settings.APP_VERSION)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application")


@app.get("/")
async def root():
    return {"message": "Welcome to KnowledgeFlow AI"}
