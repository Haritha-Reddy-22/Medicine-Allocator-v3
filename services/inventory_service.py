from sqlalchemy.orm import Session

from models.inventory import Inventory
from models.hospital import Hospital
from models.medicine import Medicine


class InventoryService:

    # -----------------------------------------
    # ADD INVENTORY
    # -----------------------------------------

    @staticmethod
    def add_inventory(
        db: Session,
        hospital_id: int,
        medicine_id: int,
        quantity: int,
        reorder_level: int
    ):

        if quantity < 0:
            return False, "Quantity cannot be negative."

        if reorder_level < 0:
            return False, "Reorder level cannot be negative."

        existing = (
            db.query(Inventory)
            .filter(
                Inventory.hospital_id == hospital_id,
                Inventory.medicine_id == medicine_id
            )
            .first()
        )

        if existing:

            existing.quantity = quantity
            existing.reorder_level = reorder_level

            db.commit()
            db.refresh(existing)

            return True, "Inventory updated successfully."

        inventory = Inventory(
            hospital_id=hospital_id,
            medicine_id=medicine_id,
            quantity=quantity,
            reorder_level=reorder_level
        )

        db.add(inventory)
        db.commit()
        db.refresh(inventory)

        return True, "Inventory added successfully."

    # -----------------------------------------
    # GET ALL INVENTORY
    # -----------------------------------------

    @staticmethod
    def get_all_inventory(db: Session):

        return (
            db.query(Inventory)
            .all()
        )

    # -----------------------------------------
    # GET LOW STOCK INVENTORY
    # -----------------------------------------

    @staticmethod
    def get_low_stock_inventory(db: Session):

        return (
            db.query(Inventory)
            .filter(
                Inventory.quantity <= Inventory.reorder_level
            )
            .all()
        )

    # -----------------------------------------
    # MEDICINE AVAILABILITY
    # -----------------------------------------

    @staticmethod
    def get_medicine_availability(
        db: Session,
        medicine_id: int
    ):

        return (
            db.query(
                Inventory,
                Hospital,
                Medicine
            )
            .join(
                Hospital,
                Inventory.hospital_id == Hospital.id
            )
            .join(
                Medicine,
                Inventory.medicine_id == Medicine.id
            )
            .filter(
                Inventory.medicine_id == medicine_id
            )
            .all()
        )