from core.database import SessionLocal
from core.security import hash_password
from models.user import User


def create_admin():

    db = SessionLocal()

    try:

        existing = (
            db.query(User)
            .filter(
                User.email == "admin@medicineallocator.com"
            )
            .first()
        )

        if existing:

            print("✅ Admin already exists.")
            return

        admin = User(

            full_name="System Administrator",

            email="admin@medicineallocator.com",

            phone="9999999999",

            password_hash=hash_password("Admin@123"),

            role="ADMIN",

            is_active=True

        )

        db.add(admin)

        db.commit()

        print("🎉 Admin account created successfully!")

        print("--------------------------------")

        print("Email    : admin@medicineallocator.com")

        print("Password : Admin@123")

        print("--------------------------------")

    finally:

        db.close()


if __name__ == "__main__":

    create_admin()