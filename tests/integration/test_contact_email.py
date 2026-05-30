import builtins

import pytest

from main import main
from src.commands.contact_email import CONTACT_EMAIL_MESSAGES
from src.utils.serializers.address_book import AddressBookSerializer


def test_main_contact_email_finds_contact_by_full_email(monkeypatch, capsys, tmp_path):
    """Перевіряє пошук контакту за повним email.

    Дано:
        Контакт із заданим повним email.
    Коли:
        Виконується команда ``contact-email`` з цим email.
    Тоді:
        У виводі відображається інформація про відповідний контакт.
    """
    file_path = str(tmp_path / "address_book.pkl")
    email = "mykhailo.zhar@stud.onu.edu.ua"
    lines = iter(
        [
            "add Mykhailo 1234567890",
            f"insert-email Mykhailo {email}",
            f"contact-email {email}",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert f"Contact name: Mykhailo, phones: 1234567890, email: {email}" in out


def test_main_contact_email_returns_first_on_collision(monkeypatch, capsys, tmp_path):
    """Перевіряє, що contact-email повертає перший контакт при колізії email.

    Дано:
        Два контакти з однаковим email; Alice додано раніше за Bob.
    Коли:
        Виконується команда ``contact-email`` зі спільним email.
    Тоді:
        У виводі лише контакт Alice; обидва записи зберігають email у книзі.
    """
    file_path = str(tmp_path / "address_book.pkl")
    serializer = AddressBookSerializer(file_path)
    shared_email = "shared@example.com"
    lines = iter(
        [
            "add Alice 1111111111",
            f"insert-email Alice {shared_email}",
            "add Bob 2222222222",
            f"insert-email Bob {shared_email}",
            f"contact-email {shared_email}",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert "Contact name: Alice" in out
    assert "Contact name: Bob" not in out

    deserialized_address_book = serializer.deserialize()
    assert deserialized_address_book.data["Alice"].email.value == shared_email
    assert deserialized_address_book.data["Bob"].email.value == shared_email


def test_main_contact_email_for_missing_email_shows_error(
    monkeypatch, capsys, tmp_path
):
    """Перевіряє помилку contact-email для відсутнього email.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується ``contact-email`` для неіснуючого email.
    Тоді:
        Показується повідомлення ``No such contact.``.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "contact-email missing@example.com",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert CONTACT_EMAIL_MESSAGES["NO_SUCH_CONTACT"] in out


@pytest.mark.parametrize(
    "command_line",
    [
        "contact-email",
        "contact-email mail@example.com extra",
    ],
)
def test_main_contact_email_wrong_arity_shows_syntax(
    monkeypatch, capsys, tmp_path, command_line
):
    """Перевіряє синтаксичну помилку для contact-email.

    Дано:
        Команда ``contact-email`` без email або з зайвими аргументами.
    Коли:
        Запускається сценарій REPL із цією командою.
    Тоді:
        Показується повідомлення про синтаксис команди ``contact-email``.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            command_line,
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert CONTACT_EMAIL_MESSAGES["INVALID_SYNTAX"] in out
