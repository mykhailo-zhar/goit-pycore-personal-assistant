import builtins

import pytest

from main import main
from src.commands.add_contact import ADD_CONTACT_MESSAGES
from src.serializers.address_book import AddressBookSerializer


@pytest.fixture
def serializer(tmp_path):
    return AddressBookSerializer(str(tmp_path / "address_book.pkl"))


def test_add_contact_success(monkeypatch, capsys, serializer):
    """Перевіряє успішне додавання нового контакту.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується команда ``add Pat 1234567890``.
    Тоді:
        Контакт зберігається у файлі та виводиться підтвердження.
    """
    lines = iter(["add Pat 1234567890", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    book = serializer.deserialize()
    record = book.find_record("Pat")
    assert record is not None
    assert record.find_phone("1234567890") is not None

    out = capsys.readouterr().out
    assert ADD_CONTACT_MESSAGES["CONTACT_ADDED"] in out


def test_add_contact_adds_phone_to_existing(monkeypatch, capsys, serializer):
    """Перевіряє додавання другого телефону до існуючого контакту.

    Дано:
        Адресна книга з контактом Pat та одним телефоном.
    Коли:
        Виконується команда ``add Pat 0987654321``.
    Тоді:
        Другий телефон додається до контакту.
    """
    lines = iter(
        [
            "add Pat 1234567890",
            "add Pat 0987654321",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    record = serializer.deserialize().find_record("Pat")
    assert record.find_phone("1234567890") is not None
    assert record.find_phone("0987654321") is not None

    out = capsys.readouterr().out
    assert ADD_CONTACT_MESSAGES["CONTACT_ADDED"] in out


def test_add_contact_duplicate_phone(monkeypatch, capsys, serializer):
    """Перевіряє помилку при дублікаті телефону в контакті.

    Дано:
        Адресна книга з контактом Pat та телефоном 1234567890.
    Коли:
        Повторно виконується ``add Pat 1234567890``.
    Тоді:
        Виводиться повідомлення про наявність телефону.
    """
    lines = iter(
        [
            "add Pat 1234567890",
            "add Pat 1234567890",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert ADD_CONTACT_MESSAGES["PHONE_ALREADY_EXISTS"] in out


@pytest.mark.parametrize(
    "command_line",
    ["add", "add Pat", "add Pat 1234567890 extra"],
)
def test_add_contact_invalid_syntax(monkeypatch, capsys, serializer, command_line):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``add`` з неправильною кількістю аргументів.
    Коли:
        Запускається інтерактивний сценарій із цією командою.
    Тоді:
        Виводиться повідомлення про невалідну команду.
    """
    lines = iter([command_line, "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert ADD_CONTACT_MESSAGES["INVALID_COMMAND"] in out
