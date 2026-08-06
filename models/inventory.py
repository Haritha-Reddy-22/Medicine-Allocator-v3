from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Inventory(Base):

    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    hospital_id: Mapped[int] = mapped_column(
        ForeignKey("hospitals.id"),
        nullable=False
    )

    medicine_id: Mapped[int] = mapped_column(
        ForeignKey("medicines.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    reorder_level: Mapped[int] = mapped_column(
        Integer,
        default=10
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    hospital = relationship("Hospital")

    medicine = relationship("Medicine")