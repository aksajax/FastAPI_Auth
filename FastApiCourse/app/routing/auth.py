from fastapi import APIRouter, Depends
from app.database.schema.user_schema import UserSchema
from app.models.todo import CreateTodo
from typing import Annotated
from app.models.auth import Register,Login
from sqlalchemy.orm import Session
from app.database.db import get_db
from fastapi import JSONResponse
from app.helpers import create_access_token, hash_password, verify_password
router =APIRouter(
    prefix="/auth",
    tags=["todos"]
)

@router.get("/")
def get_todos():
    return {"Message": "Get all todos"}

@router.post("/login")
def login(data: Login, db: Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if not user:
        return JSONResponse({"Message": "Invalid email or password"}, status_code=400)
    
    if not verify_password(data.password, user.password):
        return JSONResponse({"Message": "Invalid email or password"}, status_code=400)
    
    # If authentication is successful, you can create and return a JWT token here
    # payload = {
    #     "id": user.id,
    #     "email": user.email,
    #     "name": user.name
    # }
    access_token = create_access_token(data={"sub": user.email})
    return JSONResponse({"Message": "Login successful", "access_token": access_token})


   

@router.post("/register")
def register(data: Register, db: Annotated[Session, Depends(get_db)]):
   existing_user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
   if existing_user:
       return JSONResponse({"Message": "Email already exists"}, status_code=400)
   

     # If no existing user, create a new one
   new_user = UserSchema(
       name=data.name,
       email=data.email,
       password=hash_password(data.password)  # In a real app, you'd hash the password
   )
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return JSONResponse({"Message": "User registered successfully", "user": new_user.model_dump()})


