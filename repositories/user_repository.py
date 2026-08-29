
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
        role: str = "USER"
    ):

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            role=role.upper()
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
    def get_user_by_id(
        db: Session,
        user_id: int
    ):

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_all_users(
        db: Session
    ):

        return (
            db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

    @staticmethod
    def count_admins(
        db: Session
    ):

        return (
            db.query(User)
            .filter(User.role == "ADMIN")
            .count()
        )

    @staticmethod
    def update_role(
        db: Session,
        user_id: int,
        role: str,
        current_admin_id: int | None = None
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            return False, "User not found."

        role = role.upper()

        if role not in ["USER", "ADMIN"]:
            return False, "Invalid role."

        current_role = str(user.role).upper()

        # Already has requested role
        if current_role == role:

            return (
                False,
                f"User is already {role}."
            )

        # -----------------------------------------
        # Prevent removing the last ADMIN
        # -----------------------------------------

        if current_role == "ADMIN" and role == "USER":

            admin_count = (
                db.query(User)
                .filter(User.role == "ADMIN")
                .count()
            )

            if admin_count <= 1:

                return (
                    False,
                    "The last ADMIN cannot be demoted."
                )

        # -----------------------------------------
        # Prevent self-demotion
        # -----------------------------------------

        if (
            current_admin_id is not None
            and user.id == current_admin_id
            and current_role == "ADMIN"
            and role == "USER"
        ):

            return (
                False,
                "You cannot demote your own ADMIN account."
            )

        # -----------------------------------------
        # Update role
        # -----------------------------------------

        user.role = role

        db.commit()
        db.refresh(user)

        return (
            True,
            f"{user.full_name} is now {role}."
        )

