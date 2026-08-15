from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentInitializeResponse
from app.services.payment_service import PaymentService


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


def get_payment_service(
    db: Session = Depends(get_db),
) -> PaymentService:
    repository = PaymentRepository(db)

    return PaymentService(
        db=db,
        repository=repository,
    )


@router.post(
    "",
    response_model=PaymentInitializeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    payment: PaymentCreate,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
):
    try:
        return service.create_payment(
            user_id=current_user.id,
            order_id=payment.order_id,
            payment_method=payment.payment_method,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.post(
"/{payment_id}/verify",
response_model=PaymentResponse,
)
def verify_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
):
    try:
        return service.verify_payment(
            user_id=current_user.id,
            payment_id=payment_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )