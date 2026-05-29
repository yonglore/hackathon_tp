"""Доменные структуры данных, общие для всего проекта."""

from dataclasses import dataclass


@dataclass
class Email:
    """Одно письмо, прочитанное из папки inbox.

    Храним отдельно разобранные поля письма и полный исходный текст,
    чтобы при ошибках парсинга можно было посмотреть оригинал
    """

    path: str
    sender: str
    subject: str
    body: str
    raw: str
    is_readable: bool = True

    def text_for_classification(self) -> str:
        """Вернуть тему и тело письма для поиска ключевых слов."""

        # Классификатору важно искать совпадения и в теме, и в тексте
        return f"{self.subject}\n{self.body}".lower()