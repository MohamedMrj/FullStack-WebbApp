from pydantic import BaseModel
from pydantic.errors import EmailError
from pydantic.types import constr
from sqlalchemy import orm
from typing import Optional
#--------------------------------#
class User(BaseModel):
    id:int
    email: str
    f_name: str
    l_name: str
    presentation: Optional[constr(max_length=512)]= ""
    class Config:
        orm_mode = True
#--------------------------------#
class UserCreate(BaseModel):
    email: str
    f_name: str
    l_name: str
#--------------------------------#
class UserDelete(BaseModel):
    email:str
