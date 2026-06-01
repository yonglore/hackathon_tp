"""Точка входа приложения MailSort.
    Запуск (см. run.sh):
    py -m src.main --inbox data/inbox --out data/processed --log logs/run.log
"""

import argparse
from pathlib import Path

from .classifier import Classifier
from .config import UNREADABLE_CATEGORY
from .email_reader import read_all
from .file_organizer import organize
from .logger import setup_logger
from .stats import Statistics


def parse_args(argv=None) -> argparse.Namespace:
    """Разобрать аргументы командной строки"""

    parser = argparse.ArgumentParser(
        prog="mailsort",
        description="Автоматическая сортировка корпоративных писем по категориям",
    )
    parser.add_argument(
        "--inbox",
        default="data/inbox",
        help="Папка с входящими письмами (по умолчанию: data/inbox)",
    )
    parser.add_argument(
        "--out",
        default="data/processed",
        help="Папка для разложенных по категориям писем (по умолчанию: data/processed)",
    )
    parser.add_argument(
        "--log",
        default=None,
        help="Путь к файлу журнала. Если не задан - лог пишется только в консоль",
    )
    return parser.parse_args(argv)


def run(inbox_dir: Path, out_dir: Path, log_path=None) -> Statistics:
    """Выполнить полный цикл обработки писем и вернуть собранную статистику"""

    logger = setup_logger(log_path)

    logger.info("Запуск MailSort")
    logger.info("inbox : %s", inbox_dir)
    logger.info("out   : %s", out_dir)
    logger.info("log   : %s", log_path if log_path else "только консоль")

    #Чтение всех писем из входящей папки
    emails = read_all(Path(inbox_dir))
    logger.info("Прочитано файлов: %d", len(emails))

    if not emails:
        logger.warning("Во входящей папке нет писем для обработки: %s", inbox_dir)

    classifier = Classifier()
    stats = Statistics()

    #Обработка каждого письма
    for email in emails:
        category = classifier.classify(email)

        # Нечитаемые/повреждённые письма дополнительно учитываем как проблемные
        if not email.is_readable or category == UNREADABLE_CATEGORY:
            stats.record_error(email.path)
            logger.warning("Нечитаемое письмо -> %s: %s", UNREADABLE_CATEGORY, email.path)

        #Перемещаем файл в папку соответствующей категории
        new_path = organize(email, category, Path(out_dir))
        logger.debug("%s -> %s/%s", Path(email.path).name, category, Path(new_path).name)

        stats.record(category)

    #Выводим итоговую сводку в журнал и в консоль через логгер
    logger.info("Обработка завершена")
    for line in stats.summary().splitlines():
        logger.info(line)

    return stats


def main(argv=None) -> int:
    """Обёртка с обработкой аргументов и кодом возврата для bash-скрипта"""

    args = parse_args(argv)
    try:
        run(inbox_dir=args.inbox, out_dir=args.out, log_path=args.log)
        return 0
    except Exception as exc:
        # фиксируем ошибку в журнале и возвращаем код для run.sh.
        logger = setup_logger(args.log)
        logger.error("Критическая ошибка во время обработки: %s", exc, exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())