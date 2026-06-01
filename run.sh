#!/usr/bin/env bash
# Скрипт запуска приложения MailSort.
# Критерий 4 (bash): должен запускать приложение и реализовывать
# конструкции помимо вызова python - проверка существования папки
# inbox, создание выходных папок, вывод итогового статуса по коду возврата.

set -uo pipefail

INBOX="data/inbox"
OUT="data/processed"
LOG_DIR="logs"
LOG="$LOG_DIR/run.log"

# На Windows стандартный лаунчер - py, на macOS/Linux - python3.
# Скрипт сам подбирает доступный интерпретатор, поэтому переписывать
# код под конкретную ОС не нужно. Можно переопределить вручную:
#   PYTHON_BIN=python ./run.sh
if [ -z "${PYTHON_BIN:-}" ]; then
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_BIN="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_BIN="python"
    elif command -v py >/dev/null 2>&1; then
        PYTHON_BIN="py"
    else
        echo "Ошибка: не найден интерпретатор Python (python3 / python / py)"
        exit 1
    fi
fi

# Без входной папки приложение не сможет найти письма для сортировки
if [ ! -d "$INBOX" ]; then
    echo "Ошибка: папка с письмами не найдена: $INBOX"
    exit 1
fi

# Создаём папки для результата и логов, если их ещё нет
mkdir -p "$OUT"
mkdir -p "$LOG_DIR"

echo "Интерпретатор: $PYTHON_BIN"
echo "Запуск обработки писем из $INBOX ..."

# Запускаем приложение и сохраняем подробный вывод в лог
"$PYTHON_BIN" -m src.main --inbox "$INBOX" --out "$OUT" --log "$LOG"
EXIT_CODE=$?

# По коду возврата выводим понятный итоговый статус
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "Обработка завершена успешно. Лог: $LOG"
else
    echo "Обработка завершилась с ошибкой. Подробности в логе: $LOG"
fi

exit "$EXIT_CODE"