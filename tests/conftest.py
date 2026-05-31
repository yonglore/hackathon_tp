"""Общие фикстуры для тестов"""

import pytest
from src.models import Email


# Письмо с инцидентом
@pytest.fixture
def incident_email():

    return Email(
        path="data/inbox/mail_001.txt",
        sender="admin@example.com",
        subject="Срочно ошибка 500",
        body="Сервис не отвечает уже несколько минут",
        raw="",
    )


# Письмо от HR
@pytest.fixture
def hr_email():

    return Email(
        path="data/inbox/mail_002.txt",
        sender="hr@example.com",
        subject="Новый сотрудник",
        body="Нужно подготовить рабочее место",
        raw="",
    )


# Письмо без понятных ключевых слов
@pytest.fixture
def unknown_email():

    return Email(
        path="data/inbox/mail_003.txt",
        sender="user@example.com",
        subject="Привет",
        body="Просто обычное письмо без смысла",
        raw="",
    )


# Письмо которое не удалось прочитать
@pytest.fixture
def unreadable_email():

    return Email(
        path="data/inbox/broken.txt",
        sender="",
        subject="",
        body="",
        raw="",
        is_readable=False,
    )
