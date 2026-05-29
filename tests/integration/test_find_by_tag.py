import builtins

import pytest

from src.commands.find_by_tag import FIND_BY_TAG_MESSAGES
from src.scripts.contacts_bot import main
from src.utils.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_find_by_tag_ascending(monkeypatch, capsys, note_serializer):
    """Перевіряє сортування нотаток за зростанням заголовка."""
    lines = iter(
        [
            "add-note zebra",
            "add-tag zebra urgent",
            "add-note alpha",
            "add-tag alpha urgent",
            "tag urgent ascending",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note_book = note_serializer.deserialize()
    alpha = str(note_book.find_note("alpha"))
    zebra = str(note_book.find_note("zebra"))
    out = capsys.readouterr().out
    assert out.index(alpha) < out.index(zebra)


def test_find_by_tag_descending(monkeypatch, capsys, note_serializer):
    """Перевіряє сортування нотаток за спаданням заголовка."""
    lines = iter(
        [
            "add-note alpha",
            "add-tag alpha urgent",
            "add-note zebra",
            "add-tag zebra urgent",
            "tag urgent descending",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note_book = note_serializer.deserialize()
    alpha = str(note_book.find_note("alpha"))
    zebra = str(note_book.find_note("zebra"))
    out = capsys.readouterr().out
    assert out.index(zebra) < out.index(alpha)


def test_find_by_tag_invalid_order(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для невалідного порядку сортування."""
    lines = iter(
        ["add-note ideas", "add-tag ideas urgent", "tag urgent random", "exit"]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert FIND_BY_TAG_MESSAGES["INVALID_ORDER"] in out


def test_find_by_tag_no_notes(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку, коли нотаток з тегом немає."""
    lines = iter(["tag missing ascending", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert FIND_BY_TAG_MESSAGES["NO_NOTES"] in out


@pytest.mark.parametrize(
    "command_line",
    ["tag", "tag urgent"],
)
def test_find_by_tag_invalid_syntax(monkeypatch, capsys, note_serializer, command_line):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів."""
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert FIND_BY_TAG_MESSAGES["INVALID_SYNTAX"] in out
