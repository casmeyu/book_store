from pydantic import BaseModel
from typing import Optional

class BookSchema(BaseModel):
    id : Optional[int]
    isbn : str
    title : str
    author : str
    publisher : str
    price : int