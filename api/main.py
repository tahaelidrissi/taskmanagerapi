from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from api.models import Task  # Assure-toi que Task est bien défini dans models.py
from api.routes.tasks import router as task_router  # Router des routes

app = FastAPI()

@app.on_event("startup")
async def app_init():
    """
    Initialiser la base de données Beanie avec MongoDB
    """
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI n'est pas défini dans les variables d'environnement")

    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Task])
@app.get("/health")
async def health_check():
    return {"status": "OK"}
# Inclure les routes
app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])


