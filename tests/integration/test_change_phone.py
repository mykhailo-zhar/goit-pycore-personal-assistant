import builtins

import pytest

from main import main
from src.commands.change_phone import CHANGE_PHONE_MESSAGES
from src.record import PHONE_NOT_FOUND_ERROR
from src.utils.serializers.address_book import AddressBookSerializer


@pytest.fixture
def phone():
    return "1234567890"


@pytest.fixture
def serializer(tmp_path):
    return AddressBookSerializer(str(tmp_path / "address_book.pkl"))


def test_change_phone_success(monkeypatch, capsys, phone, serializer):
    """Перевіряє успішну зміну телефону контакту.

    Дано:
        Адресна книга з контактом Pat та телефоном 1234567890.
    Коли:
        Виконується ``change-phone Pat 1234567890 0987654321``.
    Тоді:
        Телефон оновлюється у записі та виводиться підтвердження.
    """
    new_phone = "0987654321"
    lines = iter(
        [
            f"add Pat {phone}",
            f"change-phone Pat {phone} {new_phone}",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    record = serializer.deserialize().find_record("Pat")
    assert record.find_phone(phone) is None
    assert record.find_phone(new_phone) is not None

    out = capsys.readouterr().out
    assert CHANGE_PHONE_MESSAGES["PHONE_CHANGED"] in out


def test_change_phone_no_such_user(monkeypatch, capsys, phone, serializer):
    """Перевіряє помилку для неіснуючого контакту.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується ``change-phone Ghost 1234567890 0987654321``.
    Тоді:
        Виводиться повідомлення про відсутність користувача.
    """
    lines = iter(
        [
            f"change-phone Ghost {phone} 0987654321",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert CHANGE_PHONE_MESSAGES["NO_SUCH_USER"] in out


def test_change_phone_no_such_phone(monkeypatch, capsys, phone, serializer):
    """Перевіряє помилку для неіснуючого телефону.

    Дано:
        Адресна книга з контактом Pat та одним телефоном.
    Коли:
        Виконується ``change-phone`` з неіснуючим старим номером.
    Тоді:
        Виводиться повідомлення про відсутність телефону.
    """
    other_phone = "0000000000"
    lines = iter(
        [
            f"add Pat {phone}",
            f"change-phone Pat {other_phone} 0987654321",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert PHONE_NOT_FOUND_ERROR in out


@pytest.mark.parametrize(
    "command_line",
    [
        "change-phone",
        "change-phone Pat",
        "change-phone Pat 1234567890",
        "change-phone Pat 1234567890 0987654321 extra",
    ],
)
def test_change_phone_invalid_syntax(
    monkeypatch, capsys, serializer, command_line
):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``change-phone`` з неправильною арністю.
    Коли:
        Запускається інтерактивний сценарій.
    Тоді:
        Виводиться повідомлення про синтаксис команди.
    """
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert CHANGE_PHONE_MESSAGES["PHONE_CHANGE_SYNTAX"] in out
