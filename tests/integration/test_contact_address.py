import builtins

import pytest

from main import main
from src.commands.contact_address import CONTACT_ADDRESS_MESSAGES
from src.serializers.address_book import AddressBookSerializer


@pytest.fixture
def serializer(tmp_path):
    return AddressBookSerializer(str(tmp_path / "address_book.pkl"))


def test_main_contact_address_finds_contacts_by_similarity(
    monkeypatch, capsys, tmp_path
):
    """Перевіряє пошук контактів за схожістю адреси.

    Дано:
        Контакти в Одесі та Києві.
    Коли:
        Виконується команда ``contact-address Odesa``.
    Тоді:
        У виводі лише контакти, чия адреса містить ``Odesa``.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "add Anna 1111111111",
            "insert-address Anna Odesa, Heroiv Square 1",
            "add Ivan 2222222222",
            "insert-address Ivan Kyiv, Khreshchatyk 10",
            "add Oleg 3333333333",
            "insert-address Oleg Odesa, Deribasivska 5",
            "contact-address Odesa",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert "Anna" in out
    assert "Oleg" in out
    assert "Ivan" not in out


def test_main_contact_address_supports_multi_word_search(monkeypatch, capsys, tmp_path):
    """Перевіряє contact-address з багатословним запитом.

    Дано:
        Контакти з різними адресами, одна містить ``Heroiv Square``.
    Коли:
        Виконується команда ``contact-address Heroiv Square``.
    Тоді:
        У виводі лише контакт із відповідною адресою.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "add Anna 1111111111",
            "insert-address Anna Odesa, Heroiv Square 1",
            "add Ivan 2222222222",
            "insert-address Ivan Kyiv, Khreshchatyk 10",
            "contact-address Heroiv Square",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert "Anna" in out
    assert "Ivan" not in out


def test_main_contact_address_for_missing_address_shows_error(
    monkeypatch, capsys, tmp_path
):
    """Перевіряє помилку contact-address для відсутньої адреси.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується ``contact-address Lviv``.
    Тоді:
        Показується повідомлення ``No such contact.``.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "contact-address Lviv",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert CONTACT_ADDRESS_MESSAGES["NO_SUCH_CONTACT"] in out


def test_main_contact_address_wrong_arity_shows_syntax(monkeypatch, capsys, tmp_path):
    """Перевіряє синтаксичну помилку для contact-address без аргументів.

    Дано:
        Команда ``contact-address`` без аргументів.
    Коли:
        Запускається сценарій REPL із цією командою.
    Тоді:
        Показується повідомлення про синтаксис команди ``contact-address``.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "contact-address",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert "<address>" in out
