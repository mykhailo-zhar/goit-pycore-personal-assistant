import builtins

import pytest

from src.commands.add_tag import ADD_TAG_MESSAGES
from src.scripts.contacts_bot import main
from src.utils.serializers.note_book import NoteBookSerializer


@pytest.fixture
def note_serializer(tmp_path):
    return NoteBookSerializer(str(tmp_path / "notebook.pkl"))


def test_add_tag_success(monkeypatch, capsys, note_serializer):
    """Перевіряє успішне додавання тегу.

    Дано:
        Книга нотаток із нотаткою ``ideas`` без тегів.
    Коли:
        Виконується команда ``add-tag ideas urgent``.
    Тоді:
        Виводиться підтвердження, тег ``urgent`` зберігається у нотатці.
    """
    lines = iter(["add-note ideas", "add-tag ideas urgent", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert ADD_TAG_MESSAGES["TAG_ADDED"] in out
    assert (
        note_serializer.deserialize().find_note("ideas").show_tags() == "urgent"
    )


def test_add_tag_duplicate(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку при дублікаті тегу.

    Дано:
        Книга нотаток із нотаткою ``ideas`` і тегом ``urgent``.
    Коли:
        Повторно виконується команда ``add-tag ideas urgent``.
    Тоді:
        Виводиться повідомлення про наявність такого тегу.
    """
    lines = iter(
        [
            "add-note ideas",
            "add-tag ideas urgent",
            "add-tag ideas urgent",
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
    assert ADD_TAG_MESSAGES["TAG_ALREADY_EXISTS"] in out


def test_add_tag_no_such_note(monkeypatch, capsys, note_serializer):
    """Перевіряє помилку для неіснуючої нотатки.

    Дано:
        Порожня книга нотаток.
    Коли:
        Виконується команда ``add-tag missing urgent``.
    Тоді:
        Виводиться повідомлення про відсутність нотатки.
    """
    lines = iter(["add-tag missing urgent", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert ADD_TAG_MESSAGES["NO_SUCH_NOTE"] in out


@pytest.mark.parametrize(
    "command_line",
    ["add-tag", "add-tag ideas"],
)
def test_add_tag_invalid_syntax(monkeypatch, capsys, note_serializer, command_line):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``add-tag`` з неправильною кількістю аргументів.
    Коли:
        Запускається сценарій REPL із цією командою.
    Тоді:
        Виводиться повідомлення про синтаксис команди.
    """
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.NOTE_SERIALIZER_PATH",
        note_serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert ADD_TAG_MESSAGES["INVALID_SYNTAX"] in out
