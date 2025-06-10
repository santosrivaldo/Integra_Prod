from pydantic import BaseModel
from typing import Optional

class Activity(BaseModel):
    user: str
    app: str
    start: str
    end: str
    active: Optional[bool] = True
    bucket: str
    timestamp: str