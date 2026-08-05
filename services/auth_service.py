from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository
from core.security import hash_password, verify_password


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        full_name: str,
        email: str,
        phone: str,
        password: str,
        role: str = "User"
    ):

        # Check email
        if UserRepository.get_user_by_email(db, email):
            return False, "Email already exists."

        # Check phone
        if UserRepository.get_user_by_phone(db, phone):
            return False, "Phone number already exists."

        # Hash password
        password_hash = hash_password(password)

        user = UserRepository.create_user(
            db=db,
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            role=role
        )

        return True, user

    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str
    ):

        user = UserRepository.get_user_by_email(
            db,
            email
        )

        if not user:
            return False, "User not found."

        if not verify_password(
            password,
            user.password_hash
        ):
            return False, "Incorrect password."

        return True, user