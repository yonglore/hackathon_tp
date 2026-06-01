"""Настройка логирования для приложения MailSort.
Здесь используется штатный модуль logging из стандартной библиотеки.
Это инструмент, который не разбирался на занятиях (Критерий 2). Позволяет
вести единый журнал работы приложения сразу в консоли и в
файле. Реализован единый формат строк и уровней важности (INFO / WARNING / ERROR).

Формат строки журнала:
    2026-06-01 17:58:50 [INFO] текст сообщения
"""

import logging
import sys
from pathlib import Path

# Имя логгера по умолчанию
LOGGER_NAME = "mailsort"

# Единый формат записей и формат даты
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(log_path=None, level: int = logging.INFO, name: str = LOGGER_NAME) -> logging.Logger:
    """Создание и настройка логгера приложения"""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Чтобы сообщения не дублировались, сначала убираем уже навешанные обработчики.
    if logger.handlers:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()

    logger.propagate = False

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    #Вывод в консоль чтобы видеть прогресс во время запуска.
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    #Вывод в файл - постоянный журнал работы для последующего разбора.
    if log_path is not None:
        log_path = Path(log_path)
        try:
            # Создаём папку под лог, если её ещё нет
            if log_path.parent and not log_path.parent.exists():
                log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except OSError as exc:
            # Если файл недоступен для записи - сообщаем об этом в консоль и продолжаем работать
            logger.warning("Не удалось открыть файл журнала %s: %s", log_path, exc)

    return logger


def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    """Получить уже настроенный логгер по имени (без переинициализации)."""

    return logging.getLogger(name)
