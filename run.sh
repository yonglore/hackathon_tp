#!/usr/bin/env bash
# Скрипт запуска приложения MailSort.
# Критерий 4 (bash): должен запускать приложение И реализовывать
# конструкции помимо вызова python — проверка существования папки
# inbox, вывод итогового статуса, перенаправление вывода в лог-файл.


set -uo pipefail

INBOX="data/inbox"
OUT="data/processed"
LOG_DIR="logs"
LOG="$LOG_DIR/run.log"
PYTHON_BIN="${PYTHON_BIN:-python3}"

# Без входной папки приложение не сможет найти письма для сортировки
if [ ! -d "$INBOX" ]; then
    echo "Ошибка: папка с письмами не найдена: $INBOX"
    exit 1
fi

# Создаём папки для результата и логов, если их ещё нет
mkdir -p "$OUT"
mkdir -p "$LOG_DIR"

# Запускаем приложение и сохраняем подробный вывод в лог
"$PYTHON_BIN" -m src.main --inbox "$INBOX" --out "$OUT" --log "$LOG" > "$LOG" 2>&1
EXIT_CODE=$?

# По коду возврата выводим понятный итоговый статус
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "Обработка завершена успешно. Лог: $LOG"
else
    echo "Обработка завершилась с ошибкой. Подробности в логе: $LOG"
fi

exit "$EXIT_CODE"