import os
import asyncio
import nest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from api.models import Task

nest_asyncio.apply()
from dotenv import load_dotenv
load_dotenv()


_client = None
_db = None
_is_initialized = False
_loop_id = None

async def get_database():
    global _client, _db, _is_initialized, _loop_id

    current_loop = asyncio.get_running_loop()

    if _client is None or _loop_id != id(current_loop):
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise RuntimeError("MONGO_URI n'est pas défini dans les variables d'environnement")
        _client = AsyncIOMotorClient(mongo_uri)
        _db = _client.get_default_database()
        _loop_id = id(current_loop)
        _is_initialized = False  # reset init on new loop
        print(f"Création nouveau client MongoDB pour event loop {_loop_id}")

    if not _is_initialized:
        await init_beanie(database=_db, document_models=[Task])
        _is_initialized = True
        print("✅ Beanie initialisé")

    return _db
