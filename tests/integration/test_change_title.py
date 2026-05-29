import builtins

import pytest

from src.commands.change_title import CHANGE_TITLE_MESSAGES
from src.scripts.contacts_bot import main
from src.utils.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_change_title_success(monkeypatch, capsys, note_serializer):
    """Перевіряє успішну зміну заголовка нотатки."""
    lines = iter(["add-note work", "change-title work personal", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert CHANGE_TITLE_MESSAGES["TITLE_CHANGED"] in out
    assert note_serializer.deserialize().find_note("personal") is not None


def test_change_title_no_such_note(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для неіснуючої нотатки."""
    lines = iter(["change-title missing new-title", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert CHANGE_TITLE_MESSAGES["NO_SUCH_NOTE"] in out


def test_change_title_collision(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку при зайнятому новому заголовку."""
    lines = iter(
        [
            "add-note first",
            "add-note second",
            "change-title first second",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert CHANGE_TITLE_MESSAGES["NOTE_ALREADY_EXISTS"] in out


@pytest.mark.parametrize(
    "command_line",
    ["change-title", "change-title only"],
)
def test_change_title_invalid_syntax(
    monkeypatch, capsys, note_serializer, command_line
):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів."""
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert CHANGE_TITLE_MESSAGES["INVALID_SYNTAX"] in out
