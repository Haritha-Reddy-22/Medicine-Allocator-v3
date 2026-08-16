from sqlalchemy.orm import Session

from models.hospital import Hospital
from models.inventory import Inventory
from models.medicine import Medicine


class ReportService:

    @staticmethod
    def get_hospital_report(db: Session):

        return db.query(Hospital).all()

    @staticmethod
    def get_medicine_report(db: Session):

        return db.query(Medicine).all()

    @staticmethod
    def get_inventory_report(db: Session):

        return db.query(Inventory).all()

    @staticmethod
    def get_low_stock_report(db: Session):

        return (
            db.query(Inventory)
            .filter(
                Inventory.quantity <= Inventory.reorder_level
            )
            .all()
        )

    @staticmethod
    def get_expired_report(db: Session):

        from datetime import date

        return (
            db.query(Inventory)
            .join(Medicine)
            .filter(
                Medicine.expiry_date < date.today()
            )
            .all()
        )