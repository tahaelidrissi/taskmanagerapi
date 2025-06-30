from beanie import Document
from datetime import datetime

class Task(Document):
    title: str
    description: str
    priority: int
    due_date: datetime
    completed: bool = False

