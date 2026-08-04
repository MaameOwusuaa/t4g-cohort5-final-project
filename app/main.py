from fastapi import FastAPI
from fastapi import APIRouter

app = FastAPI()
router = APIRouter()

@router.get("/")
def home():
    return {"message": "Welcome to FastAPI"}

app.include_router(router) 