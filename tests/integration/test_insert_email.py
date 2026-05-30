import builtins

import pytest

from main import main
from src.commands.add_contact import ADD_CONTACT_MESSAGES
from src.commands.exit_command import EXIT_COMMAND_MESSAGES
from src.commands.insert_email import INSERT_EMAIL_MESSAGES
from src.utils.serializers.address_book import AddressBookSerializer


def test_main_insert_email_adds_to_existing_contact(monkeypatch, capsys, tmp_path):
    """Перевіряє додавання email до існуючого контакту через інтерактивний сценарій.

    Дано:
        Існуючий контакт без email.
    Коли:
        Виконується ``insert-email``.
    Тоді:
        Email додається у запис та виводиться повідомлення про успіх.
    """
    file_path = str(tmp_path / "address_book.pkl")
    serializer = AddressBookSerializer(file_path)
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-email Pat pat@example.com",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert ADD_CONTACT_MESSAGES["CONTACT_ADDED"] in out
    assert (
        INSERT_EMAIL_MESSAGES["EMAIL_ADDED"].format(email="pat@example.com", name="Pat")
        in out
    )
    assert EXIT_COMMAND_MESSAGES["GOOD_BYE"] in out

    deserialized_address_book = serializer.deserialize()
    assert deserialized_address_book.data["Pat"].email.value == "pat@example.com"


def test_main_insert_email_replaces_existing_email(monkeypatch, capsys, tmp_path):
    """Перевіряє перезапис існуючого email через інтерактивний сценарій.

    Дано:
        Існуючий контакт з email.
    Коли:
        Виконується повторний ``insert-email`` з новим email.
    Тоді:
        Email перезаписується та виводиться повідомлення про заміну.
    """
    file_path = str(tmp_path / "address_book.pkl")
    serializer = AddressBookSerializer(file_path)
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-email Pat old@example.com",
            "insert-email Pat new@example.com",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert (
        INSERT_EMAIL_MESSAGES["EMAIL_REPLACED"].format(
            old_email="old@example.com",
            new_email="new@example.com",
            name="Pat",
        )
        in out
    )
    assert EXIT_COMMAND_MESSAGES["GOOD_BYE"] in out

    deserialized_address_book = serializer.deserialize()
    assert deserialized_address_book.data["Pat"].email.value == "new@example.com"


def test_main_insert_email_for_missing_contact_shows_error(
    monkeypatch, capsys, tmp_path
):
    """Перевіряє помилку для неіснуючого контакту через інтерактивний сценарій.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується ``insert-email`` для відсутнього контакту.
    Тоді:
        Показується повідомлення про відсутність користувача.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "insert-email Ghost ghost@example.com",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert INSERT_EMAIL_MESSAGES["NO_SUCH_USER"] in out
    assert EXIT_COMMAND_MESSAGES["GOOD_BYE"] in out


@pytest.mark.parametrize(
    "command_line",
    [
        "insert-email",
        "insert-email Pat",
        "insert-email Pat mail@example.com extra",
    ],
)
def test_main_insert_email_wrong_arity_shows_syntax(
    monkeypatch, capsys, tmp_path, command_line
):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``insert-email`` з неправильною арністю.
    Коли:
        Запускається інтерактивний сценарій.
    Тоді:
        Показується повідомлення про синтаксис для ``insert-email``.
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
    assert INSERT_EMAIL_MESSAGES["INVALID_SYNTAX"] in out
    assert EXIT_COMMAND_MESSAGES["GOOD_BYE"] in out
