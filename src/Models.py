from typing import Optional
from pydantic import BaseModel

class Pereval(BaseModel):
    user_email: str
    beauty_title: Optional[str]
    title: Optional[str]
    other_titles: Optional[str]
    level_summer: Optional[int]
    level_autumn: Optional[int]
    level_winter: Optional[int]
    level_spring: Optional[int]
    connect: Optional[str]
    add_time: Optional[str]
    coord_id: int
