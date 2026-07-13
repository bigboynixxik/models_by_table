"""
Автоматизированный тест компиляции модели SQLAlchemy в запросы.
Использует assert для программной проверки корректности маппинга.
"""
from sqlalchemy.dialects import mssql
from sqlalchemy.schema import CreateTable

from src.models.company import Company
from src.utils.logger import logger


def test_schema_compilation():
    logger.info("Запуск проверки компиляции модели Company...")

    try:
        # Компилируем модель и превращаем результат в обычную строку
        compiled_sql = str(
            CreateTable(Company.__table__).compile(dialect=mssql.dialect()))


        assert "[INN] VARCHAR(12) NOT NULL" in compiled_sql, "Ошибка: поле INN настроено неверно"
        assert "PRIMARY KEY ([INN])" in compiled_sql, "Ошибка: INN не установлен как первичный ключ"

        assert "[CompanyInfo] TEXT NULL" in compiled_sql, "Ошибка: CompanyInfo должно быть TEXT и допускать NULL"
        assert "DEFAULT sysdatetime()" in compiled_sql, "Ошибка: нет дефолтного sysdatetime() для дат"

        assert "raw_data TEXT NULL" in compiled_sql, "Ошибка: raw_data замаплено неверно"
        assert "[Status] VARCHAR(30) NOT NULL" in compiled_sql, "Ошибка: Status настроен неверно"

        logger.info("Запрос успешно сгенерирован и прошел все проверки!\n%s",
                    compiled_sql)
        logger.info("Тест пройден!")

    except AssertionError as e:
        logger.error(f"ТЕСТ ПРОВАЛЕН: {e}")
    except Exception as e:
        logger.error(f"Критический сбой при компиляции модели: {e}")
        raise


if __name__ == "__main__":
    test_schema_compilation()
