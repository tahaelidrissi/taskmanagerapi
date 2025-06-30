from fastapi import APIRouter
from ..models import Task  
from bson import ObjectId
from fastapi import HTTPException
from ..schemas import TaskCreate,TaskUpdate


router = APIRouter()

@router.get("/")
async def list_tasks():
    tasks = await Task.find_all().to_list()
    return tasks

@router.get("/{id}")
async def get_task(id: str):
    task = await Task.find_one(Task.id ==ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/")
async def add_task(task_data: TaskCreate):
    task= Task(**task_data.dict())
    await task.create()
    return task

@router.put("/{id}")
async def update_task(id: str,task_update: TaskUpdate):
    task= await Task.find_one(Task.id == ObjectId(id))
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
    task=await Task.find_one(Task.id == ObjectId(id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await task.delete()
    return {"message": "Task deleted successfully"}

@router.patch("/{id}")
async def update_partial_task(id: str,task_update: TaskUpdate):
    task=await Task.find_one(Task.id == ObjectId(id))
    if not task: 
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.dict(exclude_unset=True)  # garde seulement les champs envoyés
    for field, value in update_data.items():
        setattr(task, field, value)  # met à jour dynamiquement les champs
    await task.save()
    return task
