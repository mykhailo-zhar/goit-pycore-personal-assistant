import builtins

import pytest

from main import main
from src.commands.change_title import CHANGE_TITLE_MESSAGES
from src.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_change_title_success(monkeypatch, capsys, note_serializer):
    """Перевіряє успішну зміну заголовка нотатки.

    Дано:
        Книга нотаток із нотаткою ``work``.
    Коли:
        Виконується команда ``change-title work personal``.
    Тоді:
        Виводиться підтвердження зміни, нотатка доступна за новим заголовком.
    """
    lines = iter(["add-note work", "change-title work personal", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert CHANGE_TITLE_MESSAGES["TITLE_CHANGED"] in out
    assert note_serializer.deserialize().find_note("personal") is not None


def test_change_title_no_such_note(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для неіснуючої нотатки.

    Дано:
        Порожня книга нотаток.
    Коли:
        Виконується команда ``change-title missing new-title``.
    Тоді:
        Виводиться повідомлення про відсутність нотатки.
    """
    lines = iter(["change-title missing new-title", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert CHANGE_TITLE_MESSAGES["NO_SUCH_NOTE"] in out


def test_change_title_collision(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку при зайнятому новому заголовку.

    Дано:
        Книга нотаток із нотатками ``first`` та ``second``.
    Коли:
        Виконується команда ``change-title first second``.
    Тоді:
        Виводиться повідомлення про наявність нотатки з новим заголовком.
    """
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
        "main.NOTE_SERIALIZER_PATH",
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
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``change-title`` з неправильною кількістю аргументів.
    Коли:
        Запускається інтерактивний сценарій із цією командою.
    Тоді:
        Виводиться повідомлення про синтаксис команди.
    """
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert CHANGE_TITLE_MESSAGES["INVALID_SYNTAX"] in out
