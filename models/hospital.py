from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Hospital(Base):

    __tablename__ = "hospitals"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    hospital_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(300)
    )

    city: Mapped[str] = mapped_column(
        String(100)
    )

    state: Mapped[str] = mapped_column(
        String(100)
    )

    pincode: Mapped[str] = mapped_column(
        String(10)
    )

    contact_number: Mapped[str] = mapped_column(
        String(20)
    )

    email: Mapped[str] = mapped_column(
        String(150)
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    available_beds: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    available_doctors: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )