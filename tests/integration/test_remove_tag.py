import builtins

import pytest

from src.commands.remove_tag import REMOVE_TAG_MESSAGES
from src.scripts.contacts_bot import main
from src.utils.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_remove_tag_success(monkeypatch, capsys, note_serializer):
    """Перевіряє успішне видалення тегу."""
    lines = iter(
        [
            "add-note ideas",
            "add-tag ideas work",
            "remove-tag ideas work",
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
    assert REMOVE_TAG_MESSAGES["TAG_REMOVED"] in out
    assert note_serializer.deserialize().find_note("ideas").show_tags() == ""


def test_remove_tag_no_tag_on_note(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку, коли тег відсутній на нотатці."""
    lines = iter(["add-note ideas", "remove-tag ideas work", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert REMOVE_TAG_MESSAGES["NO_TAG_ON_NOTE"] in out


def test_remove_tag_no_such_note(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для неіснуючої нотатки."""
    lines = iter(["remove-tag missing work", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert REMOVE_TAG_MESSAGES["NO_SUCH_NOTE"] in out


@pytest.mark.parametrize(
    "command_line",
    ["remove-tag", "remove-tag ideas"],
)
def test_remove_tag_invalid_syntax(
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
    assert REMOVE_TAG_MESSAGES["INVALID_SYNTAX"] in out
