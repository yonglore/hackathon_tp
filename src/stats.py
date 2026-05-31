"""Сбор статистики по результатам обработки"""

from collections import Counter
from pathlib import Path


class Statistics:
    """Считает сколько писем попало в каждую категорию"""

    def __init__(self) -> None:
        self.counts = Counter()
        self.errors = []


    def record(self, category: str) -> None:
        """Учесть одно обработанное письмо"""

        # если категория почему то пустая
        if not category:
            category = "undefined"
        self.counts[category] += 1


    def record_error(self, path) -> None:
        """Учесть один проблемный файл"""

        self.errors.append(Path(path))


    def summary(self) -> str:
        """Вернуть текстовую сводку"""

        lines = ["=== Результаты обработки ==="]
        total = sum(self.counts.values())
        lines.append(f"Всего обработано: {total} писем")

        # сначала выводим самые частые категории
        for category, count in self.counts.most_common():
            lines.append(f"  {category}: {count}")
        lines.append(f"Ошибок: {len(self.errors)}")
        for path in self.errors:
            lines.append(f"  - {path.name}")
        return "\n".join(lines)
