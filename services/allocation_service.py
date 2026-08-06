from sqlalchemy.orm import Session

from repositories.allocation_repository import AllocationRepository


class AllocationService:

    @staticmethod
    def search_medicine(
        db: Session,
        keyword: str
    ):

        if not keyword.strip():
            return []

        inventory = AllocationRepository.search_medicine(
            db,
            keyword
        )

        # Ignore hospitals with zero stock
        inventory = [
            item
            for item in inventory
            if item.quantity > 0
        ]

        # Highest stock first
        inventory.sort(
            key=lambda x: x.quantity,
            reverse=True
        )

        return inventory