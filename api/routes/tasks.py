from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from ..models import Task  
from ..schemas import TaskCreate, TaskUpdate
import traceback

from main import init_db_once  # Import de la fonction d'initialisation

router = APIRouter()

# Option dépendance FastAPI pour init DB (plus propre)
async def ensure_db_initialized():
    await init_db_once()

@router.get("/", dependencies=[Depends(ensure_db_initialized)])
async def list_tasks():
    try:
        print("📥 Handling GET /api/v1/tasks/")
        tasks = await Task.find_all().to_list()
        return tasks
    except Exception as e:
        print("❌ ERROR in GET /tasks:")
        print("Type:", type(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", dependencies=[Depends(ensure_db_initialized)])
async def get_task(id: str):
    task = await Task.find_one(Task.id == ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", dependencies=[Depends(ensure_db_initialized)])
async def add_task(task_data: TaskCreate):
    task = Task(**task_data.dict())
    await task.create()
    return task

@router.put("/{id}", dependencies=[Depends(ensure_db_initialized)])
async def update_task(id: str, task_update: TaskUpdate):
    task = await Task.find_one(Task.id == ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = task_update.title
    task.description = task_update.description
    task.priority = task_update.priority
    task.due_date = task_update.due_date
    task.completed = task_update.completed

    await task.save()
    return task

@router.delete("/{id}", dependencies=[Depends(ensure_db_initialized)])
async def delete_task(id: str):
    task = await Task.find_one(Task.id == ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await task.delete()
    return {"message": "Task deleted successfully"}

@router.patch("/{id}", dependencies=[Depends(ensure_db_initialized)])
async def update_partial_task(id: str, task_update: TaskUpdate):
    task = await Task.find_one(Task.id == ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.dict(exclude_unset=True)  # garde seulement les champs envoyés
    for field, value in update_data.items():
        setattr(task, field, value)  # met à jour dynamiquement les champs
    await task.save()
    return task
