from urllib import request

from app.models.user import User
from app.repositories.user_repositories import UserRepository
from app.schemas import user
from app.schemas.user import UserCreate
from app.schemas.token import Token
from app.schemas.user import UserLogin
from app.core.security import verify_password, hash_password
from app.utils.security import create_access_token

print("VERIFY PASSWORD FROM:", verify_password.__module__)

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, request: UserCreate) -> User:
        """
        Register a new user.
        """

        existing_user = self.repository.get_by_email(request.email)

        if existing_user:
            raise ValueError("A user with this email already exists.")

        user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            hashed_password=hash_password(request.password),
            is_admin=False,
            is_active=True,
        )

        return self.repository.create(user)


    def login(self, request: UserLogin) -> Token:
        """
        Authenticate a user and return a JWT access token.
        """

        user = self.repository.get_by_email(request.email)


        if not user:
            raise ValueError("Invalid email or password.")


        

        print("EMAIL:", request.email)
        print("USER ID:", user.id)
        print("PASSWORD CHECK:", verify_password(
            request.password,
            user.hashed_password,
        ))
        print("USER ACTIVE:", user.is_active)
        

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password.")

        access_token = create_access_token(
            {
                "sub": str(user.id),
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )