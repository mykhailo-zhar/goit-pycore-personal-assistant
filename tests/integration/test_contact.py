import builtins

import pytest

from main import main
from src.commands.contact import CONTACT_MESSAGES
from src.commands.exit import EXIT_COMMAND_MESSAGES


def test_main_contact_shows_existing_fields_only(monkeypatch, capsys, tmp_path):
    """Перевіряє, що contact показує лише наявні поля контакту.

    Дано:
        Контакт з іменем, телефоном та email без адреси й дня народження.
    Коли:
        Виконується команда ``contact Pat``.
    Тоді:
        У виводі є ім'я, телефон і email; відсутні поля не згадуються.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-email Pat pat@example.com",
            "contact Pat",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert "Pat" in out
    assert "1234567890" in out
    assert "pat@example.com" in out
    assert "None" in out
    assert "None" in out


def test_main_contact_shows_all_fields(monkeypatch, capsys, tmp_path):
    """Перевіряє повний вивід contact для контакту з усіма полями.

    Дано:
        Контакт з телефоном, email, адресою та днем народження.
    Коли:
        Виконується команда ``contact Pat``.
    Тоді:
        У виводі відображаються всі заповнені поля контакту.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-email Pat pat@example.com",
            "insert-address Pat Odesa",
            "insert-birthday Pat 14.10.1992",
            "contact Pat",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert "Pat" in out
    assert "1234567890" in out
    assert "pat@example.com" in out
    assert "Odesa" in out
    assert "14.10.1992" in out


def test_main_contact_for_missing_contact_shows_error(monkeypatch, capsys, tmp_path):
    """Перевіряє помилку contact для неіснуючого контакту.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується команда ``contact Ghost``.
    Тоді:
        Показується повідомлення ``No such contact.`` і бот завершує роботу.
    """
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "contact Ghost",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert CONTACT_MESSAGES["NO_SUCH_CONTACT"] in out
    assert EXIT_COMMAND_MESSAGES["GOOD_BYE"] in out


@pytest.mark.parametrize(
    "command_line",
    [
        "contact",
        "contact Pat Extra",
    ],
)
def test_main_contact_wrong_arity_shows_syntax(
    monkeypatch, capsys, tmp_path, command_line
):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів contact.

    Дано:
        Команда ``contact`` без імені або з більш ніж одним аргументом.
    Коли:
        Запускається сценарій REPL із цією командою.
    Тоді:
        Показується повідомлення про синтаксис команди ``contact``.
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
    assert "<name>" in out
    assert EXIT_COMMAND_MESSAGES["GOOD_BYE"] in out
