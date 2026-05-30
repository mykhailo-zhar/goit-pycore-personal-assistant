import builtins

import pytest

from main import main
from src.commands.insert_birthday import INSERT_BIRTHDAY_MESSAGES
from src.record import BIRTHDAY_NOT_VALID_ERROR
from src.utils.serializers.address_book import AddressBookSerializer


@pytest.fixture
def serializer(tmp_path):
    return AddressBookSerializer(str(tmp_path / "address_book.pkl"))


def test_add_birthday_success(monkeypatch, capsys, serializer):
    """Перевіряє успішне додавання дня народження.

    Дано:
        Адресна книга з контактом Pat без дня народження.
    Коли:
        Виконується ``add-birthday Pat 14.10.1992``.
    Тоді:
        День народження зберігається у записі.
    """
    birthday = "14.10.1992"
    lines = iter(
        [
            "add Pat 1234567890",
            f"insert-birthday Pat {birthday}",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    record = serializer.deserialize().find_record("Pat")
    assert record.birthday is not None
    assert record.birthday.value == birthday

    out = capsys.readouterr().out
    assert (
        INSERT_BIRTHDAY_MESSAGES["BIRTHDAY_ADDED"].format(
            old_birthday=None,
            new_birthday=birthday,
            name="Pat",
        )
        in out
    )


def test_add_birthday_replaces_existing(monkeypatch, capsys, serializer):
    """Перевіряє заміну існуючого дня народження.

    Дано:
        Адресна книга з контактом Pat та днем народження.
    Коли:
        Виконується ``insert-birthday Pat 01.01.2000``.
    Тоді:
        День народження оновлюється у записі.
    """
    old_birthday = "14.10.1992"
    new_birthday = "01.01.2000"
    lines = iter(
        [
            "add Pat 1234567890",
            f"insert-birthday Pat {old_birthday}",
            f"insert-birthday Pat {new_birthday}",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    record = serializer.deserialize().find_record("Pat")
    assert record.birthday.value == new_birthday

    out = capsys.readouterr().out
    assert (
        INSERT_BIRTHDAY_MESSAGES["BIRTHDAY_ADDED"].format(
            old_birthday=old_birthday,
            new_birthday=new_birthday,
            name="Pat",
        )
        in out
    )


def test_add_birthday_no_such_user(monkeypatch, capsys, serializer):
    """Перевіряє помилку для неіснуючого контакту.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується ``insert-birthday Ghost 14.10.1992``.
    Тоді:
        Виводиться повідомлення про відсутність користувача.
    """
    lines = iter(["insert-birthday Ghost 14.10.1992", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert INSERT_BIRTHDAY_MESSAGES["NO_SUCH_USER"] in out


def test_add_birthday_invalid_date(monkeypatch, capsys, serializer):
    """Перевіряє помилку для невалідної дати народження.

    Дано:
        Адресна книга з контактом Pat.
    Коли:
        Виконується ``add-birthday Pat 32.13.1992``.
    Тоді:
        Виводиться повідомлення про невалідну дату.
    """
    invalid_birthday = "32.13.1992"
    lines = iter(
        [
            "add Pat 1234567890",
            f"insert-birthday Pat {invalid_birthday}",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert BIRTHDAY_NOT_VALID_ERROR.format(birthday=invalid_birthday) in out


@pytest.mark.parametrize(
    "command_line",
    ["insert-birthday", "insert-birthday Pat", "insert-birthday Pat 14.10.1992 extra"],
)
def test_add_birthday_invalid_syntax(monkeypatch, capsys, serializer, command_line):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``insert-birthday`` з неправильною арністю.
    Коли:
        Запускається інтерактивний сценарій.
    Тоді:
        Виводиться повідомлення про невалідну команду.
    """
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert INSERT_BIRTHDAY_MESSAGES["INVALID_COMMAND"] in out
