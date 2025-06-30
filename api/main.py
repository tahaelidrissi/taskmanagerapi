from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from api.models import Task  # Assure-toi que c'est bien le bon chemin
from api.routes.tasks import router as task_router

app = FastAPI()

@app.on_event("startup")
async def init_db():
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI n'est pas défini dans les variables d'environnement")
    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Task])

app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])

@app.get("/health")
async def health_check():
    return {"status": "OK"}
