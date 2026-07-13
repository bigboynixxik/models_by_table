import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.repository.company_repo import CompanyRepository
from src.utils.logger import logger

# URL
# Формат: mssql+aioodbc://логин:пароль@хост:порт/имя_бд?driver=ODBC+Driver+17+for+SQL+Server
TEST_DB_URL = "mssql+aioodbc://sa:password@localhost:1433/test_db?driver=ODBC+Driver+17+for+SQL+Server"


async def run_test():
    logger.info("Создаем асинхронный движок SQLAlchemy...")
    engine = create_async_engine(TEST_DB_URL, echo=True)

    # Создаем фабрику сессий
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    logger.info("Открываем сессию и инициализируем репозиторий...")
    async with session_maker() as session:
        repo = CompanyRepository(session)

        logger.info("Пробуем выполнить запрос get_all()...")
        try:
            # Пытаемся получить данные
            companies = await repo.get_all()
            logger.info(f"Найдено компаний: {len(companies)}")

            # Если база пустая, попробуем проверить маппинг полей первого объекта
            if companies:
                first_company = companies[0]
                logger.info(
                    f"Первая компания: ИНН={first_company.inn}, Статус={first_company.status}")

        except Exception as e:
            # Если БД нет, скрипт упадет с ошибкой подключения
            logger.error(
                "Не удалось подключиться к БД")
            logger.error(f"Текст ошибки: {e}")

    logger.info("Закрываем соединения...")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_test())
