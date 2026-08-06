from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.user_dependencies import get_user_service
from app.services.user_service import UserService
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.schemas.token import Token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return service.register(user)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
def login_user(
    credentials: UserLogin,
    service: UserService = Depends(get_user_service),
):
    try:
        return service.login(credentials)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )