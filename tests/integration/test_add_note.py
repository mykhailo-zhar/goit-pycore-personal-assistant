import builtins

import pytest

from src.commands.add_note import ADD_NOTE_MESSAGES
from src.scripts.contacts_bot import main
from src.utils.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_add_note_success(monkeypatch, capsys, note_serializer):
    """Перевіряє успішне додавання порожньої нотатки."""
    lines = iter(["add-note my-note", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note_book = note_serializer.deserialize()
    assert note_book.find_note("my-note") is not None


def test_add_note_duplicate(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку при дублікаті заголовка."""
    lines = iter(["add-note my-note", "add-note my-note", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert ADD_NOTE_MESSAGES["NOTE_ALREADY_PRESENT"] in out


@pytest.mark.parametrize(
    "command_line",
    ["add-note", "add-note a b"],
)
def test_add_note_invalid_syntax(monkeypatch, capsys, note_serializer, command_line):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів."""
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert ADD_NOTE_MESSAGES["INVALID_SYNTAX"] in out
