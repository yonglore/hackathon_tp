"""Тесты статистики"""

from pathlib import Path
from src.stats import Statistics


def test_statistics_starts_empty():

    stats = Statistics()

    assert stats.counts == {}
    assert stats.errors == []


def test_record_adds_category():

    stats = Statistics()
    stats.record("incidents")

    assert stats.counts["incidents"] == 1


def test_record_counts_same_category_several_times():

    stats = Statistics()
    stats.record("hr")
    stats.record("hr")
    stats.record("incidents")

    assert stats.counts["hr"] == 2
    assert stats.counts["incidents"] == 1


def test_record_error_saves_path():

    stats = Statistics()
    stats.record_error("data/inbox/broken.txt")
    assert stats.errors == [Path("data/inbox/broken.txt")]


def test_summary_contains_total_and_categories():

    stats = Statistics()
    stats.record("incidents")
    stats.record("incidents")
    stats.record("hr")
    summary = stats.summary()

    assert "Всего обработано: 3 писем" in summary
    assert "incidents: 2" in summary
    assert "hr: 1" in summary


def test_summary_contains_errors():

    stats = Statistics()
    stats.record("undefined")
    stats.record_error("data/inbox/broken.txt")
    summary = stats.summary()

    assert "Ошибок: 1" in summary
    assert "broken.txt" in summary
