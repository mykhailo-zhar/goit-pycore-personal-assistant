import builtins

import pytest

from main import main
from src.commands.insert_text import INSERT_TEXT_MESSAGES
from src.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_insert_text_success(monkeypatch, capsys, note_serializer):
    """Перевіряє додавання багатослівного тексту до нотатки.

    Дано:
        Книга нотаток із нотаткою ``work`` без тексту.
    Коли:
        Виконується команда ``insert-text work First line of notes``.
    Тоді:
        У нотатці зберігається повний текст із пробілами.
    """
    lines = iter(
        [
            "add-note work",
            "insert-text work First line of notes",
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
    assert note.text.value == "First line of notes"


def test_insert_text_no_text(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку, коли текст не передано.

    Дано:
        Книга нотаток із нотаткою ``work``.
    Коли:
        Виконується команда ``insert-text work`` без тексту.
    Тоді:
        Виводиться повідомлення про відсутність тексту.
    """
    lines = iter(["add-note work", "insert-text work", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert INSERT_TEXT_MESSAGES["NO_TEXT"] in out


def test_insert_text_no_such_note(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для неіснуючої нотатки.

    Дано:
        Порожня книга нотаток.
    Коли:
        Виконується команда ``insert-text missing some text``.
    Тоді:
        Виводиться повідомлення про відсутність нотатки.
    """
    lines = iter(["insert-text missing some text", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert INSERT_TEXT_MESSAGES["NO_SUCH_NOTE"] in out


def test_insert_text_invalid_syntax(monkeypatch, capsys, note_serializer):
    """Перевіряє синтаксичну помилку без аргументів.

    Дано:
        Команда ``insert-text`` без аргументів.
    Коли:
        Запускається інтерактивний сценарій.
    Тоді:
        Виводиться повідомлення про синтаксис команди.
    """
    lines = iter(["insert-text", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert "<title>" in out
