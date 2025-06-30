from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from api.models import Task  # Assure-toi que Task est bien défini dans models.py
from api.routes.tasks import router as task_router  # Router des routes

app = FastAPI()

@app.on_event("startup")
async def app_init():
    print("✅ App initialization started")

    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        print("❌ MONGO_URI not found in environment variables")
        raise RuntimeError("MONGO_URI n'est pas défini dans les variables d'environnement")

    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_default_database()
    
    print("🔗 Connecting to MongoDB...")
    await init_beanie(database=db, document_models=[Task])
    print("✅ Beanie initialized with Task model")
@app.get("/health")
async def health_check():
    return {"status": "OK"}
# Inclure les routes
app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])


