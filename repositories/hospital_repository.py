from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.hospital import Hospital


class HospitalRepository:

    @staticmethod
    def create_hospital(db: Session, hospital: Hospital):

        db.add(hospital)
        db.commit()
        db.refresh(hospital)

        return hospital

    @staticmethod
    def get_all_hospitals(db: Session):

        return (
            db.query(Hospital)
            .order_by(Hospital.hospital_name)
            .all()
        )

    @staticmethod
    def search_hospitals(db: Session, keyword: str):

        return (
            db.query(Hospital)
            .filter(
                or_(
                    Hospital.hospital_name.ilike(f"%{keyword}%"),
                    Hospital.city.ilike(f"%{keyword}%"),
                    Hospital.state.ilike(f"%{keyword}%")
                )
            )
            .order_by(Hospital.hospital_name)
            .all()
        )

    @staticmethod
    def get_hospital_by_id(db: Session, hospital_id: int):

        return (
            db.query(Hospital)
            .filter(Hospital.id == hospital_id)
            .first()
        )

    @staticmethod
    def update_hospital(db: Session, hospital: Hospital):

        db.commit()
        db.refresh(hospital)

        return hospital

    @staticmethod
    def delete_hospital(db: Session, hospital: Hospital):

        db.delete(hospital)
        db.commit()