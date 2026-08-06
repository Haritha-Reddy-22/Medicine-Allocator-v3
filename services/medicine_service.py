from sqlalchemy.orm import Session

from models.medicine import Medicine
from repositories.medicine_repository import MedicineRepository


class MedicineService:

    @staticmethod
    def add_medicine(
        db: Session,
        medicine_name: str,
        generic_name: str,
        category: str,
        manufacturer: str,
        batch_number: str,
        expiry_date,
        unit_price: float,
        description: str
    ):

        if not medicine_name.strip():
            return False, "Medicine name is required."

        if not generic_name.strip():
            return False, "Generic name is required."

        if not category.strip():
            return False, "Category is required."

        if not manufacturer.strip():
            return False, "Manufacturer is required."

        if unit_price < 0:
            return False, "Unit price cannot be negative."

        medicine = Medicine(
            medicine_name=medicine_name,
            generic_name=generic_name,
            category=category,
            manufacturer=manufacturer,
            batch_number=batch_number,
            expiry_date=expiry_date,
            unit_price=unit_price,
            description=description
        )

        MedicineRepository.create_medicine(
            db,
            medicine
        )

        return True, "Medicine Added Successfully."

    @staticmethod
    def get_all_medicines(
        db: Session
    ):

        return MedicineRepository.get_all_medicines(db)

    @staticmethod
    def search_medicines(
        db: Session,
        keyword: str
    ):

        return MedicineRepository.search_medicines(
            db,
            keyword
        )

    @staticmethod
    def get_medicine_by_id(
        db: Session,
        medicine_id: int
    ):

        return MedicineRepository.get_medicine_by_id(
            db,
            medicine_id
        )

    @staticmethod
    def update_medicine(
        db: Session,
        medicine_id: int,
        medicine_name: str,
        generic_name: str,
        category: str,
        manufacturer: str,
        unit_price: float,
        description: str
    ):

        medicine = MedicineRepository.get_medicine_by_id(
            db,
            medicine_id
        )

        if not medicine:
            return False, "Medicine not found."

        medicine.medicine_name = medicine_name
        medicine.generic_name = generic_name
        medicine.category = category
        medicine.manufacturer = manufacturer
        medicine.unit_price = unit_price
        medicine.description = description

        MedicineRepository.update_medicine(
            db,
            medicine
        )

        return True, "Medicine Updated Successfully."

    @staticmethod
    def delete_medicine(
        db: Session,
        medicine_id: int
    ):

        medicine = MedicineRepository.get_medicine_by_id(
            db,
            medicine_id
        )

        if not medicine:
            return False, "Medicine not found."

        MedicineRepository.delete_medicine(
            db,
            medicine
        )

        return True, "Medicine Deleted Successfully."