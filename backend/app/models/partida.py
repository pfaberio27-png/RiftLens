from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class Partida(Base):

    __tablename__ = "Partidas"

    partida_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    match_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    queue_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    modo: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    duracion_segundos: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    fecha_partida: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )

    estadisticas = relationship(
        "EstadisticaPartida",
        back_populates="partida",
    )