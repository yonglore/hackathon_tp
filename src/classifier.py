"""Классификация писем по категориям"""

from .config import CATEGORIES, DEFAULT_CATEGORY, UNREADABLE_CATEGORY
from .models import Email


class Classifier:
    """Классификатор писем по ключевым словам"""


    def __init__(self, rules=None) -> None:
        # если правила не передали берем основные из config.py
        if rules is None:
            self.rules = CATEGORIES
        else:
            self.rules = rules


    def classify(self, email: Email) -> str:
        """Вернуть категорию письма"""

        try:
            # плохие файлы сразу кидаем в отдельную категорию
            if not email.is_readable:
                return UNREADABLE_CATEGORY

            text = email.text_for_classification()

            for category, keywords in self.rules.items():
                # эти категории нужны как запасные варианты
                if category in (DEFAULT_CATEGORY, UNREADABLE_CATEGORY):
                    continue
                for keyword in keywords:
                    keyword = keyword.lower()
                    if keyword in text:
                        return category
            return DEFAULT_CATEGORY

        except Exception:
            # если что то сломалось просто отправляем письмо в undefined
            return DEFAULT_CATEGORY
