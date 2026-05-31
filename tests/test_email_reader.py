import os
from email_reader import read_one, read_all
from models import Email


def test_read_valid_email(tmpdir):
    file_path = os.path.join(str(tmpdir), "valid.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("From: ivan@example.com\nSubject: Hello\nBody text here")

    email = read_one(file_path)

    assert email.is_readable is True
    assert email.sender == "ivan@example.com"
    assert email.subject == "Hello"
    assert email.body == "Body text here"


def test_read_empty_email(tmpdir):
    file_path = os.path.join(str(tmpdir), "empty.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("   ")

    email = read_one(file_path)

    assert email.is_readable is False
    assert email.subject == "Empty"


def test_read_all_folder(tmpdir):
    file1 = os.path.join(str(tmpdir), "email1.txt")
    with open(file1, "w", encoding="utf-8") as f:
        f.write("From: a\nSubject: b\nbody")

    file2 = os.path.join(str(tmpdir), "email2.txt")
    with open(file2, "w", encoding="utf-8") as f:
        f.write("")

    emails = read_all(str(tmpdir))

    assert len(emails) == 2
