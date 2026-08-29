
from getpass import getpass

from core.database import SessionLocal
from core.security import hash_password
from repositories.user_repository import UserRepository


def main():

    print()
    print("======================================")
    print("     MEDICINE ALLOCATOR ADMIN SETUP")
    print("======================================")
    print()

    full_name = input("Admin Full Name: ").strip()
    email = input("Admin Email: ").strip().lower()
    phone = input("Admin Phone: ").strip()

    password = getpass("Admin Password: ")
    confirm_password = getpass("Confirm Password: ")

    # -----------------------------------
    # Basic validation
    # -----------------------------------

    if not full_name:
        print("❌ Full name is required.")
        return

    if not email:
        print("❌ Email is required.")
        return

    if not phone:
        print("❌ Phone number is required.")
        return

    if not password:
        print("❌ Password is required.")
        return

    if password != confirm_password:
        print("❌ Passwords do not match.")
        return

    db = SessionLocal()

    try:

        # -----------------------------------
        # Check whether email already exists
        # -----------------------------------

        existing_email = UserRepository.get_user_by_email(
            db,
            email
        )

        # -----------------------------------
        # Existing user
        # -----------------------------------

        if existing_email:

            print()
            print("⚠️ An account with this email already exists.")
            print()
            print(f"Name        : {existing_email.full_name}")
            print(f"Email       : {existing_email.email}")
            print(f"Current Role: {existing_email.role}")
            print()

            # Already an admin
            if str(existing_email.role).upper() == "ADMIN":

                print("ℹ️ This account is already an ADMIN.")
                print("No changes were made.")
                return

            # Existing USER
            if str(existing_email.role).upper() == "USER":

                confirmation = input(
                    "Promote this USER account to ADMIN? (yes/no): "
                ).strip().lower()

                if confirmation not in ["yes", "y"]:

                    print()
                    print("ℹ️ No changes were made.")
                    return

                existing_email.role = "ADMIN"

                db.commit()
                db.refresh(existing_email)

                print()
                print("======================================")
                print("       ✅ ADMIN PROMOTION SUCCESS")
                print("======================================")
                print()
                print(f"Name : {existing_email.full_name}")
                print(f"Email: {existing_email.email}")
                print(f"Role : {existing_email.role}")
                print()
                print("You can now log in using this account.")
                print()

                return

            print(
                f"❌ Unsupported existing role: "
                f"{existing_email.role}"
            )

            return

        # -----------------------------------
        # Check phone number
        # -----------------------------------

        existing_phone = UserRepository.get_user_by_phone(
            db,
            phone
        )

        if existing_phone:

            print()
            print(
                "❌ A user with this phone number already exists."
            )
            print()
            print(f"Existing Name : {existing_phone.full_name}")
            print(f"Existing Email: {existing_phone.email}")
            print(f"Current Role  : {existing_phone.role}")
            print()

            return

        # -----------------------------------
        # Create first ADMIN
        # -----------------------------------

        password_hash = hash_password(
            password
        )

        admin = UserRepository.create_user(
            db=db,
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            role="ADMIN"
        )

        print()
        print("======================================")
        print("       ✅ ADMIN ACCOUNT CREATED")
        print("======================================")
        print()
        print(f"Name : {admin.full_name}")
        print(f"Email: {admin.email}")
        print(f"Role : {admin.role}")
        print()
        print("You can now log in using this account.")
        print()

    except Exception as e:

        db.rollback()

        print()
        print("======================================")
        print("          ❌ ADMIN SETUP FAILED")
        print("======================================")
        print()
        print(f"Error: {e}")
        print()

    finally:

        db.close()


if __name__ == "__main__":
    main()

