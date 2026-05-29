import builtins

import pytest

from src.commands.insert_address import INSERT_ADDRESS_MESSAGES
from src.scripts.contacts_bot import main
from src.utils.serializers.address_book import AddressBookSerializer


@pytest.fixture
def serializer(tmp_path):
    return AddressBookSerializer(str(tmp_path / "address_book.pkl"))


def test_insert_address_success(monkeypatch, capsys, serializer):
    """Перевіряє успішне додавання адреси контакту.

    Дано:
        Адресна книга з контактом Pat без адреси.
    Коли:
        Виконується команда insert-address Pat Kyiv.
    Тоді:
        Для контакту зберігається адреса Kyiv і повертається повідомлення про додавання.
    """
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-address Pat Kyiv",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert INSERT_ADDRESS_MESSAGES["ADDRESS_ADDED"] in out
    assert serializer.deserialize().find_record("Pat").address.value == "Kyiv"


def test_insert_address_replaces_existing(monkeypatch, capsys, serializer):
    """Перевіряє заміну існуючої адреси контакту.

    Дано:
        Адресна книга з контактом Pat і адресою Kyiv.
    Коли:
        Виконується команда insert-address Pat Lviv.
    Тоді:
        Адреса Pat змінюється на Lviv і повертається повідомлення про заміну.
    """
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-address Pat Kyiv",
            "insert-address Pat Lviv",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert (
        INSERT_ADDRESS_MESSAGES["ADDRESS_REPLACED"].format(
            old_address="Kyiv",
            new_address="Lviv",
            name="Pat",
        )
        in out
    )


def test_insert_address_non_existent_contact(monkeypatch, capsys):
    """Перевіряє обробку неіснуючого контакту.

    Дано:
        Адресна книга без контакту Pat.
    Коли:
        Виконується команда insert-address Pat Kyiv.
    Тоді:
        Повертається повідомлення про відсутність контакту.
    """
    lines = iter(
        [
            "insert-address Pat Kyiv",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    main()

    out = capsys.readouterr().out
    assert INSERT_ADDRESS_MESSAGES["NO_SUCH_CONTACT"] in out
