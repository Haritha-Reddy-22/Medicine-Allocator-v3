from core.database import SessionLocal
from services.auth_service import AuthService

db = SessionLocal()

success, result = AuthService.register_user(
    db=db,
    full_name="Haritha Reddy",
    email="haritha@gmail.com",
    phone="9999999999",
    password="Haritha@123"
)

print(success)
print(result)

print("----------------")

success, result = AuthService.login_user(
    db=db,
    email="haritha@gmail.com",
    password="Haritha@123"
)

print(success)
print(result.full_name if success else result)

db.close()