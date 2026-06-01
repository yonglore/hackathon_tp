import os
from src.file_organizer import organize
from src.models import Email


def test_organize_moves_file(tmpdir):
    base_dir = str(tmpdir)
    inbox_dir = os.path.join(base_dir, "inbox")
    os.makedirs(inbox_dir)

    email_file = os.path.join(inbox_dir, "spam_letter.txt")
    with open(email_file, "w", encoding="utf-8") as f:
        f.write("From: spammer\nSubject: Buy now\nClick here")

    email_obj = Email(
        path=email_file,
        sender="spammer",
        subject="Buy now",
        body="Click here",
        raw="...",
        is_readable=True
    )

    out_dir = os.path.join(base_dir, "processed")

    new_path = organize(email_obj, "spam", out_dir)

    assert os.path.exists(new_path)
    assert os.path.basename(os.path.dirname(new_path)) == "spam"
    assert not os.path.exists(email_file)


def test_organize_handles_collision(tmpdir):
    base_dir = str(tmpdir)
    inbox_dir = os.path.join(base_dir, "inbox")
    os.makedirs(inbox_dir)

    email_file = os.path.join(inbox_dir, "letter.txt")
    with open(email_file, "w", encoding="utf-8") as f:
        f.write("New content")

    email_obj = Email(email_file, "user", "hi", "text", "...", True)
    out_dir = os.path.join(base_dir, "processed")

    target_dir = os.path.join(out_dir, "work")
    os.makedirs(target_dir)

    existing_file = os.path.join(target_dir, "letter.txt")
    with open(existing_file, "w", encoding="utf-8") as f:
        f.write("Old content")

    new_path = organize(email_obj, "work", out_dir)

    assert os.path.basename(new_path) == "letter_1.txt"
    assert os.path.exists(existing_file)
    assert os.path.exists(new_path)
