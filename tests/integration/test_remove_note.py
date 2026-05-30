import builtins

import pytest

from main import main
from src.commands.remove_note import REMOVE_NOTE_MESSAGES
from src.utils.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_remove_note_success(monkeypatch, capsys, note_serializer):
    """Перевіряє успішне видалення нотатки.

    Дано:
        Книга нотаток із нотаткою ``my-note``.
    Коли:
        Виконується ``remove-note my-note``.
    Тоді:
        Нотатка видаляється з файлу та виводиться відповідь команди.
    """
    lines = iter(["add-note my-note", "remove-note my-note", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.NOTE_SERIALIZER_PATH", note_serializer.file_path)
    main()

    note_book = note_serializer.deserialize()
    assert note_book.find_note("my-note") is None

    out = capsys.readouterr().out
    assert REMOVE_NOTE_MESSAGES["NOTE_ALREADY_DELETED"] in out


def test_remove_note_not_found(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для неіснуючої нотатки.

    Дано:
        Порожня книга нотаток.
    Коли:
        Виконується ``remove-note missing``.
    Тоді:
        Виводиться повідомлення про відсутність нотатки.
    """
    lines = iter(["remove-note missing", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.NOTE_SERIALIZER_PATH", note_serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert REMOVE_NOTE_MESSAGES["NOTE_NOT_FOUND"] in out


@pytest.mark.parametrize(
    "command_line",
    ["remove-note", "remove-note a b"],
)
def test_remove_note_invalid_syntax(
    monkeypatch, capsys, note_serializer, command_line
):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``remove-note`` з неправильною кількістю аргументів.
    Коли:
        Запускається інтерактивний сценарій.
    Тоді:
        Виводиться повідомлення про синтаксис команди.
    """
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.NOTE_SERIALIZER_PATH", note_serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert REMOVE_NOTE_MESSAGES["INVALID_SYNTAX"] in out
