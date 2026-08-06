from sqlalchemy.orm import Session

from models.inventory import Inventory
from models.hospital import Hospital
from models.medicine import Medicine


class AllocationRepository:

    @staticmethod
    def search_medicine(
        db: Session,
        keyword: str
    ):

        return (

            db.query(Inventory)

            .join(
                Hospital,
                Inventory.hospital_id == Hospital.id
            )

            .join(
                Medicine,
                Inventory.medicine_id == Medicine.id
            )

            .filter(
                Medicine.medicine_name.ilike(
                    f"%{keyword}%"
                )
            )

            .all()

        )