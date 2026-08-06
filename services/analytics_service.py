from sqlalchemy import func
from sqlalchemy.orm import Session

from models.hospital import Hospital
from models.inventory import Inventory
from models.medicine import Medicine


class AnalyticsService:

    @staticmethod
    def inventory_by_hospital(db: Session):

        data = (
            db.query(
                Hospital.hospital_name,
                func.sum(Inventory.quantity)
            )
            .join(
                Inventory,
                Hospital.id == Inventory.hospital_id
            )
            .group_by(
                Hospital.hospital_name
            )
            .all()
        )

        return data

    @staticmethod
    def medicine_category_distribution(db: Session):

        data = (
            db.query(
                Medicine.category,
                func.count(Medicine.id)
            )
            .group_by(
                Medicine.category
            )
            .all()
        )

        return data

    @staticmethod
    def stock_status_distribution(db: Session):

        inventory = db.query(Inventory).all()

        high = 0
        medium = 0
        low = 0

        for item in inventory:

            if item.quantity > 100:
                high += 1

            elif item.quantity > item.reorder_level:
                medium += 1

            else:
                low += 1

        return {
            "High Stock": high,
            "Medium Stock": medium,
            "Low Stock": low
        }