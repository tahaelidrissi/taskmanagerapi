from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
import asyncio

from api.models import Task  # modèle Beanie
from api.routes.tasks import router as task_router

app = FastAPI()

# ✅ Initialisation Beanie manuellement au moment du chargement
async def init():
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI n'est pas défini")
    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Task])

# Appelle init() via asyncio en dehors d’un event FastAPI
loop = asyncio.get_event_loop()
loop.run_until_complete(init())

@app.get("/health")
async def health_check():
    return {"status": "OK"}

# Routers
app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])


