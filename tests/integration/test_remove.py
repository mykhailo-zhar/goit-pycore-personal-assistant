import builtins

import pytest

from main import main
from src.commands.remove_contact import REMOVE_CONTACT_MESSAGES
from src.serializers.address_book import AddressBookSerializer


@pytest.fixture
def phone():
    return "1234567890"


@pytest.fixture
def serializer(tmp_path):
    return AddressBookSerializer(str(tmp_path / "address_book.pkl"))


def test_remove_contact(monkeypatch, capsys, phone, serializer):
    """Перевіряє видалення контакту з адресної книги.

    Дано:
        Завантажена адресна книга з двома телефонами для контакту Pat.
    Коли:
        Запускається команда ``remove Pat``.
    Тоді:
        Контакт Pat видаляється з адресної книги.
    """
    lines = iter(
        [
            f"add Pat {phone}",
            "remove Pat",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out

    assert REMOVE_CONTACT_MESSAGES["CONTACT_REMOVED"].format(name="Pat") in out
    deserialized_address_book = serializer.deserialize()
    assert len(deserialized_address_book.data) == 0


def test_remove_phone(monkeypatch, capsys, phone, serializer):
    """Перевіряє видалення телефону з контакту.

    Дано:
        Завантажена адресна книга з одним телефоном для контакту Pat.
    Коли:
        Виконується команда ``remove Pat`` з номером телефону контакту.
    Тоді:
        Телефон видаляється з контакту Pat.
    """
    lines = iter(
        [
            f"add Pat {phone}",
            f"remove Pat {phone}",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out

    assert (
        REMOVE_CONTACT_MESSAGES["PHONE_REMOVED"].format(phone=phone, name="Pat") in out
    )
    deserialized_address_book = serializer.deserialize()
    assert len(deserialized_address_book.data) == 1
    assert deserialized_address_book.find_record("Pat").find_phone(phone) is None


def test_remove_non_existent_contact(monkeypatch, capsys, phone, serializer):
    """Перевіряє видалення неіснуючого контакту.

    Дано:
        Завантажена адресна книга без записів.
    Коли:
        Запускається команда ``remove Pat``.
    Тоді:
        Виводиться повідомлення про відсутність контакту.
    """

    lines = iter(
        [
            f"remove Pat {phone}",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert REMOVE_CONTACT_MESSAGES["CONTACT_NOT_FOUND"].format(name="Pat") in out


def test_remove_non_existent_phone(monkeypatch, capsys, phone, serializer):
    """Перевіряє видалення неіснуючого телефону.

    Дано:
        Завантажена адресна книга з одним телефоном для контакту Pat.
    Коли:
        Запускається команда ``remove Pat`` з неіснуючим номером телефону.
    Тоді:
        Виводиться повідомлення про відсутність телефону.
    """
    other_phone = "0000000000"

    lines = iter(
        [
            f"add Pat {phone}",
            f"remove Pat {other_phone}",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "main.SERIALIZER_PATH",
        serializer.file_path,
    )
    main()

    out = capsys.readouterr().out
    assert (
        REMOVE_CONTACT_MESSAGES["PHONE_NOT_FOUND"].format(phone=other_phone, name="Pat")
        in out
    )
    deserialized_address_book = serializer.deserialize()
    assert len(deserialized_address_book.data) == 1
    assert deserialized_address_book.find_record("Pat").find_phone(phone) is not None


@pytest.mark.parametrize(
    "remove_command", ["remove", "remove Pat 1234567890 1234567890"]
)
def test_remove_contact_with_invalid_syntax(monkeypatch, capsys, remove_command):
    """Перевіряє видалення контакту з неправильним синтаксисом.

    Дано:
        Завантажена адресна книга з одним телефоном для контакту Pat.
    Коли:
        Запускається команда ``remove`` з неправильним синтаксисом.
    Тоді:
        Виводиться повідомлення про синтаксичну помилку.
    """
    lines = iter(
        [
            remove_command,
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    main()

    out = capsys.readouterr().out
    assert REMOVE_CONTACT_MESSAGES["INVALID_SYNTAX"] in out
