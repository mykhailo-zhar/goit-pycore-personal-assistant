import builtins

import pytest

from main import main
from src.commands.show_note import SHOW_NOTE_MESSAGES
from src.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_show_note_title_only(monkeypatch, capsys, note_serializer):
    """Перевіряє виведення нотатки лише з заголовком.

    Дано:
        Книга нотаток із порожньою нотаткою ``work``.
    Коли:
        Виконується команда ``note work``.
    Тоді:
        У виводі з'являється рядкове подання нотатки з заголовком.
    """
    lines = iter(["add-note work", "note work", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note = note_serializer.deserialize().find_note("work")
    expected = str(note)
    out = capsys.readouterr().out
    assert expected in out


def test_show_note_full(monkeypatch, capsys, note_serializer):
    """Перевіряє виведення нотатки з текстом і тегами.

    Дано:
        Книга нотаток із нотаткою ``work``, текстом і тегом ``urgent``.
    Коли:
        Виконується команда ``note work``.
    Тоді:
        У виводі з'являється повне рядкове подання нотатки.
    """
    lines = iter(
        [
            "add-note work",
            "insert-text work Hello",
            "add-tag work urgent",
            "note work",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    note = note_serializer.deserialize().find_note("work")
    expected = str(note)
    out = capsys.readouterr().out
    assert expected in out


def test_show_note_no_such_note(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для неіснуючої нотатки.

    Дано:
        Порожня книга нотаток.
    Коли:
        Виконується команда ``note missing``.
    Тоді:
        Виводиться повідомлення про відсутність нотатки.
    """
    lines = iter(["note missing", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert SHOW_NOTE_MESSAGES["NO_SUCH_NOTE"] in out


def test_show_note_invalid_syntax(monkeypatch, capsys, note_serializer):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``note`` без аргументів.
    Коли:
        Запускається інтерактивний сценарій.
    Тоді:
        Виводиться повідомлення про синтаксис команди.
    """
    lines = iter(["note", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert SHOW_NOTE_MESSAGES["INVALID_SYNTAX"] in out
