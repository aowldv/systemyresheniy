"""
Модуль логирования.

Настраивает единый логгер для всего проекта: пишет и в консоль,
и в файл run.log с временными метками и уровнем важности.
"""
import logging
import sys
from pathlib import Path


def setup_logger(name: str = "wolfram_lab", log_file: str = "run.log") -> logging.Logger:
    """
    Создаёт и настраивает логгер.

    :param name: имя логгера
    :param log_file: путь к файлу лога
    :return: настроенный объект Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Чтобы не дублировать обработчики при повторном вызове
    if logger.handlers:
        return logger

    # Формат сообщений: время | уровень | сообщение
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Обработчик: запись в файл
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Обработчик: вывод в консоль (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
