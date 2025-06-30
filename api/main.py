from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from api.models import Task
from api.routes.tasks import router as task_router

app = FastAPI()

@app.on_event("startup")
async def app_init():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI non défini dans les variables d'environnement")
    
    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Task])

@app.get("/health")
async def health_check():
    return {"status": "OK"}

app.include_router(task_router)
