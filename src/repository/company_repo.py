from typing import Sequence, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.company import Company
from src.utils.logger import logger


class CompanyRepository:
    """
    Репозиторий для работы с таблицей компаний.
    Отвечает за SQL-запросы к модели Company.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория.
        :param session: Асинхронная сессия SQLAlchemy
        """
        self.session = session

    async def get_by_inn(self, inn: str) -> Optional[Company]:
        """
        Найти компанию по ИНН.

        :param inn: Строка с ИНН компании (до 12 символов).
        :return: Объект Company или None, если компания не найдена.
        """
        try:
            stmt = select(Company).where(Company.inn == inn)
            result = await self.session.execute(stmt)

            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Ошибка при поиске компании по ИНН {inn}: {e}")
            raise

    async def get_by_status(self, status: str) -> Sequence[Company]:
        """
        Найти все компании с указанным статусом.

        :param status: Строка статуса.
        :return: Список объектов Company.
        """
        try:
            stmt = select(Company).where(Company.status == status)
            result = await self.session.execute(stmt)

            return result.scalars().all()
        except Exception as e:
            logger.error(
                f"Ошибка при поиске компаний со статусом '{status}': {e}")
            raise

    async def get_all(self) -> Sequence[Company]:
        """
        Получить все записи о компаниях из БД.
        Для очень больших таблиц стоит использовать пагинацию (limit/offset).

        :return: Список всех объектов Company.
        """
        try:
            # Строим запрос: SELECT * FROM companies
            stmt = select(Company)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Ошибка при получении всех компаний: {e}")
            raise
