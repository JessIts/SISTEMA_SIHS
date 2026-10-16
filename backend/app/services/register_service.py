from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.register import RegisterRequest
from app.services.user_service import UserService


class RegisterService:

    def __init__(self, db: Session):
        self.user_service = UserService(db)

    def register(
        self,
        data: RegisterRequest,
    ) -> User:

        user_data = UserCreate(
            name=data.name,
            email=data.email,
            phone=data.phone,
            document_number=data.document_number,
            password=data.password,
        )

        return self.user_service.create_user(user_data)