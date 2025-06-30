from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
import asyncio

from api.models import Task
from api.routes.tasks import router as task_router

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "OK"}

# Inclure les routes
app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])

# ✅ Initialiser Beanie immédiatement (hors événement startup)
async def init():
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI n'est pas défini dans les variables d'environnement")
    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Task])

# ✅ Lance l'initialisation
asyncio.run(init())
