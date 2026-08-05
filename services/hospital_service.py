from sqlalchemy.orm import Session

from models.hospital import Hospital
from repositories.hospital_repository import HospitalRepository


class HospitalService:

    @staticmethod
    def add_hospital(
        db: Session,
        hospital_name: str,
        address: str,
        city: str,
        state: str,
        pincode: str,
        contact_number: str,
        email: str,
        latitude: float,
        longitude: float,
        available_beds: int,
        available_doctors: int
    ):

        if not hospital_name.strip():
            return False, "Hospital name is required."

        if not city.strip():
            return False, "City is required."

        hospital = Hospital(
            hospital_name=hospital_name,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            contact_number=contact_number,
            email=email,
            latitude=latitude,
            longitude=longitude,
            available_beds=available_beds,
            available_doctors=available_doctors
        )

        HospitalRepository.create_hospital(
            db,
            hospital
        )

        return True, "Hospital Added Successfully."

    @staticmethod
    def get_all_hospitals(db: Session):

        return HospitalRepository.get_all_hospitals(db)

    @staticmethod
    def search_hospitals(
        db: Session,
        keyword: str
    ):

        return HospitalRepository.search_hospitals(
            db,
            keyword
        )

    @staticmethod
    def get_hospital_by_id(
        db: Session,
        hospital_id: int
    ):

        return HospitalRepository.get_hospital_by_id(
            db,
            hospital_id
        )

    @staticmethod
    def delete_hospital(
        db: Session,
        hospital_id: int
    ):

        hospital = HospitalRepository.get_hospital_by_id(
            db,
            hospital_id
        )

        if not hospital:
            return False, "Hospital not found."

        HospitalRepository.delete_hospital(
            db,
            hospital
        )

        return True, "Hospital Deleted Successfully."

    @staticmethod
    def update_hospital(
        hospital_id: int,
        db: Session,
        hospital_name: str,
        city: str,
        state: str,
        available_beds: int,
        available_doctors: int
    ):

        hospital = HospitalRepository.get_hospital_by_id(
            db,
            hospital_id
        )

        if not hospital:
            return False, "Hospital not found."

        hospital.hospital_name = hospital_name
        hospital.city = city
        hospital.state = state
        hospital.available_beds = available_beds
        hospital.available_doctors = available_doctors

        HospitalRepository.update_hospital(
            db,
            hospital
        )

        return True, "Hospital Updated Successfully."