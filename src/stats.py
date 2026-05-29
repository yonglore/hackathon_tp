"""Сбор статистики по результатам обработки.

Данные отсюда используются в итоговом выводе и могут лечь в основу расширения
(отчёт/визуализация — критерий 7).

TODO: реализовать.
"""


class Statistics:
    """Накопитель статистики за один запуск.

    TODO:
        - считать обработанные письма по категориям;
        - считать ошибки/нечитаемые файлы;
        - метод summary() возвращает сводку для вывода в консоль/лог.
    """

    def __init__(self) -> None:
        # TODO: инициализировать счётчики
        raise NotImplementedError

    def record(self, category: str) -> None:
        """Учесть одно обработанное письмо. TODO."""
        raise NotImplementedError

    def record_error(self, path) -> None:
        """Учесть один проблемный файл. TODO."""
        raise NotImplementedError

    def summary(self) -> str:
        """Вернуть текстовую сводку. TODO."""
        raise NotImplementedError
