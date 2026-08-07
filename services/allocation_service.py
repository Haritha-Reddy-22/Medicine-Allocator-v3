from sqlalchemy.orm import Session

from repositories.allocation_repository import AllocationRepository
from utils.distance import DistanceCalculator


class AllocationService:

    @staticmethod
    def search_medicine(
        db: Session,
        keyword: str,
        user_latitude: float = None,
        user_longitude: float = None
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

        # If user location is available,
        # calculate distance and sort by nearest hospital
        if (
            user_latitude is not None
            and user_longitude is not None
        ):

            for item in inventory:

                item.distance = DistanceCalculator.haversine(
                    user_latitude,
                    user_longitude,
                    item.hospital.latitude,
                    item.hospital.longitude
                )

            inventory.sort(
                key=lambda x: x.distance
            )

        else:

            # Default sorting by stock
            inventory.sort(
                key=lambda x: x.quantity,
                reverse=True
            )

        return inventory