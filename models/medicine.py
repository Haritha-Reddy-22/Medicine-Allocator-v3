from datetime import datetime

from sqlalchemy import Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Medicine(Base):

    __tablename__ = "medicines"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    medicine_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    generic_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    manufacturer: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    batch_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    expiry_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    unit_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )