from fastapi import FastAPI
import asyncio
from .database import init_db
from .routes.tasks import router as task_router

app = FastAPI(title="TaskManagerAPI")
app.include_router(task_router)
# Démarrage de l'application
@app.on_event("startup")
async def on_startup():
    await init_db()

# Endpoint simple de vérification
@app.get("/health")
async def health_check():
    return {"status": "OK"}
