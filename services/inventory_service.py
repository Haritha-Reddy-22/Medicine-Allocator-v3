from sqlalchemy.orm import Session

from models.inventory import Inventory
from repositories.inventory_repository import InventoryRepository


class InventoryService:

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

        existing = InventoryRepository.get_inventory_by_hospital_and_medicine(
            db,
            hospital_id,
            medicine_id
        )

        # If inventory already exists, increase stock
        if existing:

            existing.quantity += quantity
            existing.reorder_level = reorder_level

            InventoryRepository.update_inventory(
                db,
                existing
            )

            return True, "Inventory updated successfully."

        # Otherwise create a new record
        inventory = Inventory(
            hospital_id=hospital_id,
            medicine_id=medicine_id,
            quantity=quantity,
            reorder_level=reorder_level
        )

        InventoryRepository.create_inventory(
            db,
            inventory
        )

        return True, "Inventory added successfully."

    @staticmethod
    def get_all_inventory(
        db: Session
    ):

        return InventoryRepository.get_all_inventory(db)

    @staticmethod
    def get_inventory_by_id(
        db: Session,
        inventory_id: int
    ):

        return InventoryRepository.get_inventory_by_id(
            db,
            inventory_id
        )

    @staticmethod
    def update_inventory(
        db: Session,
        inventory_id: int,
        quantity: int,
        reorder_level: int
    ):

        inventory = InventoryRepository.get_inventory_by_id(
            db,
            inventory_id
        )

        if not inventory:
            return False, "Inventory not found."

        inventory.quantity = quantity
        inventory.reorder_level = reorder_level

        InventoryRepository.update_inventory(
            db,
            inventory
        )

        return True, "Inventory updated successfully."

    @staticmethod
    def delete_inventory(
        db: Session,
        inventory_id: int
    ):

        inventory = InventoryRepository.get_inventory_by_id(
            db,
            inventory_id
        )

        if not inventory:
            return False, "Inventory not found."

        InventoryRepository.delete_inventory(
            db,
            inventory
        )

        return True, "Inventory deleted successfully."

    @staticmethod
    def get_low_stock_inventory(
        db: Session
    ):

        inventory_items = InventoryRepository.get_all_inventory(db)

        return [
            item
            for item in inventory_items
            if item.quantity <= item.reorder_level
        ]