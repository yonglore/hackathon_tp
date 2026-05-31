"""Перемещение файлов писем в папки соответствующих категорий.
Критерий 3 (файловая система и исключения).
"""

from pathlib import Path

from .models import Email


def organize(email: Email, category: str, out_dir: Path) -> Path:
    """Переместить файл письма в out_dir/<category>/ и вернуть новый путь."""

    try:
        src_path = Path(email.path)
        if not src_path.exists():
            return src_path

        target_dir = out_dir / category
        target_dir.mkdir(parents=True, exist_ok=True)

        filename = src_path.name
        new_path = target_dir / filename

        counter = 1
        while new_path.exists():
            new_path = target_dir / f"{src_path.stem}_{counter}{src_path.suffix}"
            counter += 1

        src_path.rename(new_path)
        return new_path

    except Exception:
        return Path(email.path)