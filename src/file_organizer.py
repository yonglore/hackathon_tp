"""Перемещение файлов писем в папки соответствующих категорий.
Критерий 3 (файловая система и исключения).
"""

from pathlib import Path

from .models import Email


def organize(email: Email, category: str, out_dir: Path) -> Path:
    """Переместить файл письма в out_dir/<category>/ и вернуть новый путь."""

    try:
        # проверка сущетсвет ли
        src_path = Path(email.path)
        if not src_path.exists():
            return src_path

        # создание папки для указанной категории
        target_dir = out_dir / category
        target_dir.mkdir(parents=True, exist_ok=True)

        # формирование начального пути для перемещения
        filename = src_path.name
        new_path = target_dir / filename

        # генерация уникального имени, если файл уже существует
        count = 1
        while new_path.exists():
            new_path = target_dir / f"{src_path.stem}_{count}{src_path.suffix}"
            count += 1

        # перемещение файла на диске
        src_path.rename(new_path)
        return new_path

    except Exception:
        # возврат пути если падает ошибка
        return Path(email.path)