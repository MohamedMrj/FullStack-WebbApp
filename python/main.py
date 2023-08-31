
from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List, Optional
from fastapi.applications import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import session
from Users import schemas, models, database
from Users.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
#--------------------------------#
app = FastAPI()
#-------------------------------#

app.add_middleware(
    CORSMiddleware,
    allow_origins = "*",
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"],
)

models.Base.metadata.create_all(engine)
#------------------------------#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#--------------------------------#
@app.get('/users/{user_id}', response_model=schemas.User)
def Read_User(user_id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user
#--------------------------------#
@app.post('/users/', response_model=schemas.User)
def Create_User(request: schemas.UserCreate,db: Session = Depends(get_db)):
    new_user = models.User(email=request.email, f_name=request.f_name, l_name=request.l_name, presentation="No presentation")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user    
#--------------------------------#
@app.get('/users/', response_model=List[schemas.User])
def Read_Users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
#--------------------------------#
@app.delete('/users/', response_model=schemas.UserDelete)
def Delete_user(request:schemas.UserDelete, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.email == request.email).delete()
    db.commit()
    return request
#--------------------------------#
@app.put('/users/', response_model=schemas.User)
def Update_User(request:schemas.User, db: Session = Depends(get_db)):
    user =db.query(models.User).filter(models.User.id==request.id)
    user.update(request.dict())
    db.commit()
    return request
#--------------------------------#