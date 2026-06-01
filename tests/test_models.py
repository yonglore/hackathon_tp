"""Тесты для модели почты"""

from src.models import Email

def test_email_stores_main_fields():
    """Email должен сохранять основные данные письма без изменений"""
    email = Email(
        path="data/inbox/mail_067.txt",
        sender="boris@ochkrutoi.com",
        subject="Ошибка VPN",
        body="VPN не подключается с утра",
        raw="From: petua@parkinson.com\nSubject: Ошибка VPN\n\nVPN не подключается с утра",
    )

    assert email.path == "data/inbox/mail_067.txt"
    assert email.sender == "timakab@luk.com"
    assert email.subject == "Ошибка VPN"
    assert email.body == "VPN не подключается с утра"
    assert email.is_readable is True


def test_email_can_be_marked_as_not_readable():
    """Если файл не удалось прочитать, это должно быть видно по is_readable"""
    email = Email(
        path="data/inbox/broken_mail.txt",
        sender="",
        subject="",
        body="",
        raw="",
        is_readable=False,
    )

    assert email.is_readable is False


def test_text_for_classification_uses_subject_and_body():
    """Для классификации должны использоваться и тема, и тело письма"""
    email = Email(
        path="data/inbox/mail_666.txt",
        sender="washee@rassvet.com",
        subject="Срочная ошибка",
        body="Не работает корпоративный VPN",
        raw="",
    )

    text = email.text_for_classification()

    assert "срочная ошибка" in text
    assert "не работает корпоративный vpn" in text


def test_text_for_classification_converts_text_to_lowercase():
    """Нижний регистр нужен, чтобы поиск ключевых слов не зависел от регистра"""
    email = Email(
        path="data/inbox/mail_148.txt",
        sender="vadimkrasava@fake.com",
        subject="ОШИБКА ДОСТУПА",
        body="ПРОПАЛИ ПРАВА",
        raw="",
    )

    assert email.text_for_classification() == "ошибка доступа\nпропали права"