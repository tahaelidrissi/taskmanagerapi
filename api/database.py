from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from .models import Task
import os
from dotenv import load_dotenv

load_dotenv()  # charge les variables d’environnement du fichier .env

async def init_db():
    # Connexion à MongoDB
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))

    # Initialisation de Beanie avec le modèle Task
    await init_beanie(database=client.get_default_database(), document_models=[Task])
