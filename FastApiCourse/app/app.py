from fastapi import FastAPI,Depends
from app.routing import todo, auth
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.config.app_config import get_app_config
# from dotenv import load_dotenv
# import os


app= FastAPI()
# load_dotenv()
# include All routers
app.include_router(todo.router)
app.include_router(auth.router)

@app.exception_handler(RequestValidationError)
async def Validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(),"body":exc.body},
    )


@app.get("/")

def root():
    config = get_app_config()
    return{
        "message":"Hello World",
        "app_name":config.app_name,
        "app_env":config.app_env,
        }