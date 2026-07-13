from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Базовый класс для моделей
class BaseModel(DeclarativeBase):
    pass


class Company(BaseModel):
    """
    Модель компании
    """
    # TODO: Заменить на реальное имя таблицы
    __tablename__ = 'companies'
    # TODO: Если схема отличается от dbo, то раскомментировать строку ниже
    # __table_args__ = {"schema": "schema_name"}

    inn: Mapped[str] = mapped_column(
        "INN", String(12), primary_key=True, nullable=False
    )

    company_info: Mapped[Optional[str]] = mapped_column(
        "CompanyInfo", Text, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt", DateTime, nullable=False,
        server_default=func.sysdatetime()
    )

    updated_at: Mapped[datetime] = mapped_column(
        "UpdatedAt", DateTime, nullable=False,
        server_default=func.sysdatetime()
    )

    company_info_parse_html: Mapped[Optional[str]] = mapped_column(
        "CompanyInfoParse", Text, nullable=True
    )

    status: Mapped[str] = mapped_column(
        "Status", String(30), nullable=False
    )

    raw_data_html: Mapped[Optional[str]] = mapped_column(
        "raw_data", Text, nullable=True
    )

    raw_ukd_html: Mapped[Optional[str]] = mapped_column(
        "raw_ukd", Text, nullable=True
    )

    ukd_info: Mapped[Optional[str]] = mapped_column(
        "UKDInfoParse", Text, nullable=True
    )

    target: Mapped[Optional[str]] = mapped_column(
        "Target", String(50), nullable=True
    )
