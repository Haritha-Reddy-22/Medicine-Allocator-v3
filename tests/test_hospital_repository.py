from core.database import SessionLocal
from models.hospital import Hospital
from repositories.hospital_repository import HospitalRepository

db = SessionLocal()

hospital = Hospital(
    hospital_name="Apollo Hospital",
    address="Jubilee Hills",
    city="Hyderabad",
    state="Telangana",
    pincode="500033",
    contact_number="9876543210",
    email="apollo@test.com",
    latitude=17.4239,
    longitude=78.4738,
    available_beds=120,
    available_doctors=45
)

HospitalRepository.create_hospital(
    db,
    hospital
)

print("Hospital Added!")

print(HospitalRepository.get_all_hospitals(db))

db.close()