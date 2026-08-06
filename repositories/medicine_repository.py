from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.medicine import Medicine


class MedicineRepository:

    @staticmethod
    def create_medicine(
        db: Session,
        medicine: Medicine
    ):

        db.add(medicine)
        db.commit()
        db.refresh(medicine)

        return medicine

    @staticmethod
    def get_all_medicines(
        db: Session
    ):

        return (
            db.query(Medicine)
            .order_by(Medicine.medicine_name)
            .all()
        )

    @staticmethod
    def search_medicines(
        db: Session,
        keyword: str
    ):

        return (
            db.query(Medicine)
            .filter(
                or_(
                    Medicine.medicine_name.ilike(f"%{keyword}%"),
                    Medicine.generic_name.ilike(f"%{keyword}%"),
                    Medicine.category.ilike(f"%{keyword}%"),
                    Medicine.manufacturer.ilike(f"%{keyword}%")
                )
            )
            .order_by(Medicine.medicine_name)
            .all()
        )

    @staticmethod
    def get_medicine_by_id(
        db: Session,
        medicine_id: int
    ):

        return (
            db.query(Medicine)
            .filter(Medicine.id == medicine_id)
            .first()
        )

    @staticmethod
    def update_medicine(
        db: Session,
        medicine: Medicine
    ):

        db.commit()
        db.refresh(medicine)

        return medicine

    @staticmethod
    def delete_medicine(
        db: Session,
        medicine: Medicine
    ):

        db.delete(medicine)
        db.commit()