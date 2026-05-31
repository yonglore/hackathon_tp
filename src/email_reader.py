"""Чтение и парсинг писем из папки inbox.

Отвечает за критерий 3 (файловая система и исключения): разные форматы,
неожиданные кодировки, нечитаемые/повреждённые файлы(приложение не должно ломаться)"""

from pathlib import Path

from .models import Email


def read_all(inbox_dir: Path) -> list[Email]:
    """Прочитать все письма из inbox_dir и вернуть список Emails."""

    emails = []

    if not inbox_dir.exists() or not inbox_dir.is_dir():
        return emails

    for path in inbox_dir.iterdir():
        if path.is_file():
            try:
                email_obj = read_one(path)
                emails.append(email_obj)
            except Exception:
                continue

    return emails


def read_one(path: Path) -> Email:
    """Прочитать одно письмо"""

    raw_content = ""

    for enc in ['utf-8', 'cp1251', 'latin-1']:
        try:
            raw_content = path.read_text(encoding=enc)
            break

        except Exception:
            continue
    else:
        try:
            raw_content = path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            return Email(str(path), "Unknown", "Error", "Файл поврежден", "", is_readable=False)

    if not raw_content.strip():
        return Email(str(path), "Unknown", "Empty", "Файл пуст", "", is_readable=False)

    lines = raw_content.splitlines()

    if len(lines) > 0:
        sender = lines[0].replace("From:", "").strip()
    else:
        sender = "Unknown"

    if len(lines) > 1:
        subject = lines[1].replace("Subject:", "").strip()
    else:
        subject = "No Subject"

    if len(lines) > 2:
        body = "\n".join(lines[2:]).strip()
    else:
        body = ""

    return Email(
        path=str(path),
        sender=sender,
        subject=subject,
        body=body,
        raw=raw_content,
        is_readable=True
    )
