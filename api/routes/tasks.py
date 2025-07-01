from fastapi import APIRouter, HTTPException
from bson import ObjectId
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate
from ..database import get_database
import traceback

router = APIRouter()

@router.get("/")
async def list_tasks():
    await get_database()
    try:
        tasks = await Task.find_all().to_list()
        return tasks
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
async def get_task(id: str):
    await get_database()
    task = await Task.find_one(Task.id == ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/")
async def add_task(task_data: TaskCreate):
    await get_database()
    task = Task(**task_data.dict())
    await task.create()
    return task

@router.put("/{id}")
async def update_task(id: str, task_update: TaskUpdate):
    await get_database()
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

@router.delete("/{id}")
async def delete_task(id: str):
    await get_database()
    task = await Task.find_one(Task.id == ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await task.delete()
    return {"message": "Task deleted successfully"}

@router.patch("/{id}")
async def update_partial_task(id: str, task_update: TaskUpdate):
    await get_database()
    task = await Task.find_one(Task.id == ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    await task.save()
    return task
