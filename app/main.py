from fastapi import FastAPI
from fastapi import APIRouter

app = FastAPI(title="Conniecomes Beauty Salon API", version="1.0.0", description="API for Conniecomes Beauty Salon")
router = APIRouter()


@router.get("/")
def home():
    return {"message": "Welcome to Conniecomes Beauty Salon API!"}

app.include_router(router) 