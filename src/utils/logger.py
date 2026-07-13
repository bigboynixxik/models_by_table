"""
Модуль логирования.
Настраивает один логер на весь проект.
"""
import logging
import os


class RelativePathFilter(logging.Filter):
    """
    Фильтр, который обрезает абсолютный путь к файлу
    до относительного от корня проекта.
    """

    def __init__(self, project_root: str):
        super().__init__()
        self.project_root = project_root

    def filter(self, record: logging.LogRecord) -> bool:
        relative = os.path.relpath(record.pathname, self.project_root)
        record.pathname = relative.replace("\\", "/")
        return True


# Поднимаемся от src/utils на две папки вверх — это корень проекта
project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Создаём логер с именем "app"
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Проверяем, что обработчик ещё не добавлен (защита от дублей)
if not logger.handlers:
    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(pathname)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    handler.addFilter(RelativePathFilter(project_root))
    logger.addHandler(handler)
