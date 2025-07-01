from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from api.models import Task
import os
import asyncio
import nest_asyncio

nest_asyncio.apply()


app = FastAPI()

# Variables globales pour cache de connexion
is_initialized = False
client = None
db = None

async def init_db_once():
    global client, db, is_initialized
    if not is_initialized:
        import nest_asyncio
        nest_asyncio.apply()

        import os
        from motor.motor_asyncio import AsyncIOMotorClient
        from beanie import init_beanie
        from api.models import Task

        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise RuntimeError("MONGO_URI n'est pas défini")

        client = AsyncIOMotorClient(mongo_uri)
        db = client.get_default_database()

        await init_beanie(database=db, document_models=[Task])
        is_initialized = True
        print("✅ Beanie initialisé")


@app.get("/health")
async def health_check():
    await init_db_once()
    return {"status": "OK"}

from api.routes.tasks import router as task_router

app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])
