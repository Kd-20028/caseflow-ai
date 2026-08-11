from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    priority: Mapped[str] = mapped_column(
        String(50),
        default="medium",
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="open",
        nullable=False
    )

    sentiment: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    ai_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    assigned_team: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
