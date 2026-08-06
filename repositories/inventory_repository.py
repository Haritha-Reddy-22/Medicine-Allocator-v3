from sqlalchemy.orm import Session

from models.inventory import Inventory


class InventoryRepository:

    @staticmethod
    def create_inventory(
        db: Session,
        inventory: Inventory
    ):

        db.add(inventory)
        db.commit()
        db.refresh(inventory)

        return inventory

    @staticmethod
    def get_all_inventory(
        db: Session
    ):

        return (
            db.query(Inventory)
            .all()
        )

    @staticmethod
    def get_inventory_by_id(
        db: Session,
        inventory_id: int
    ):

        return (
            db.query(Inventory)
            .filter(Inventory.id == inventory_id)
            .first()
        )

    @staticmethod
    def get_inventory_by_hospital_and_medicine(
        db: Session,
        hospital_id: int,
        medicine_id: int
    ):

        return (
            db.query(Inventory)
            .filter(
                Inventory.hospital_id == hospital_id,
                Inventory.medicine_id == medicine_id
            )
            .first()
        )

    @staticmethod
    def update_inventory(
        db: Session,
        inventory: Inventory
    ):

        db.commit()
        db.refresh(inventory)

        return inventory

    @staticmethod
    def delete_inventory(
        db: Session,
        inventory: Inventory
    ):

        db.delete(inventory)
        db.commit()