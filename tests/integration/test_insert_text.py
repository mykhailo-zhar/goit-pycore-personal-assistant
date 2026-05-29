import builtins

import pytest

from src.commands.insert_text import INSERT_TEXT_MESSAGES
from src.scripts.contacts_bot import main
from src.utils.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_insert_text_success(monkeypatch, capsys, note_serializer):
    """Перевіряє додавання багатослівного тексту до нотатки."""
    lines = iter(
        [
            "add-note work",
            "insert-text work First line of notes",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note = note_serializer.deserialize().find_note("work")
    assert note.text.value == "First line of notes"


def test_insert_text_no_text(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку, коли текст не передано."""
    lines = iter(["add-note work", "insert-text work", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert INSERT_TEXT_MESSAGES["NO_TEXT"] in out


def test_insert_text_no_such_note(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для неіснуючої нотатки."""
    lines = iter(["insert-text missing some text", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert INSERT_TEXT_MESSAGES["NO_SUCH_NOTE"] in out


def test_insert_text_invalid_syntax(monkeypatch, capsys, note_serializer):
    """Перевіряє синтаксичну помилку без аргументів."""
    lines = iter(["insert-text", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert INSERT_TEXT_MESSAGES["INVALID_SYNTAX"] in out
