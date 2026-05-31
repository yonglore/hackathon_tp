"""Тесты классификатора"""

from src.classifier import Classifier
from src.config import DEFAULT_CATEGORY, UNREADABLE_CATEGORY


def test_classifier_finds_category_by_subject(incident_email):

    classifier = Classifier()
    assert classifier.classify(incident_email) == "incidents"


def test_classifier_finds_category_by_body(hr_email):

    classifier = Classifier()
    assert classifier.classify(hr_email) == "hr"


def test_classifier_returns_default_for_unknown_email(unknown_email):

    classifier = Classifier()
    assert classifier.classify(unknown_email) == DEFAULT_CATEGORY


def test_classifier_returns_unreadable_for_bad_email(unreadable_email):

    classifier = Classifier()
    assert classifier.classify(unreadable_email) == UNREADABLE_CATEGORY


def test_classifier_can_use_custom_rules(unknown_email):
    # можно передать свои правила

    rules = {
        "test_category": ["обычное письмо"],
    }
    classifier = Classifier(rules=rules)
    assert classifier.classify(unknown_email) == "test_category"


def test_classifier_does_not_crash_on_bad_object():

    classifier = Classifier()
    result = classifier.classify(None)
    assert result == DEFAULT_CATEGORY
