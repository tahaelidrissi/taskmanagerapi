from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
    
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int
    due_date: datetime
    completed: bool = False  
