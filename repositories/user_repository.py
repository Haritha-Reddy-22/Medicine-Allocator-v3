from sqlalchemy.orm import Session

from models.user import User


class UserRepository:

    @staticmethod
    def create_user(
        db: Session,
        full_name: str,
        email: str,
        phone: str,
        password_hash: str,
        role: str = "User"
    ):

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            role=role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_user_by_phone(
        db: Session,
        phone: str
    ):

        return (
            db.query(User)
            .filter(User.phone == phone)
            .first()
        )

    @staticmethod
    def get_all_users(
        db: Session
    ):

        return db.query(User).all()