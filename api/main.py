from fastapi import FastAPI
from api.routes.tasks import router as task_router
from api.database import get_database

app = FastAPI()

@app.get("/health")
async def health_check():
    await get_database()  # vérifie/init DB
    return {"status": "OK"}

app.include_router(task_router, prefix="/api/v1/tasks", tags=["Tasks"])
