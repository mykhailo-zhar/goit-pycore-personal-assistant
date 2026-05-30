import builtins

import pytest

from src.commands.contact import CONTACT_MESSAGES
from src.scripts.contacts_bot import COMMAND_MESSAGES, main


def test_main_contact_shows_existing_fields_only(monkeypatch, capsys, tmp_path):
    """Перевіряє, що contact показує лише наявні поля контакту."""
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
    monkeypatch.setattr("src.scripts.contacts_bot.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert "Pat" in out
    assert "1234567890" in out
    assert "pat@example.com" in out
    assert "None" in out
    assert "None" in out


def test_main_contact_shows_all_fields(monkeypatch, capsys, tmp_path):
    """Перевіряє повний вивід contact для контакту з усіма полями."""
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-email Pat pat@example.com",
            "add-address Pat Odesa",
            "add-birthday Pat 14.10.1992",
            "contact Pat",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("src.scripts.contacts_bot.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert "Pat" in out
    assert "1234567890" in out
    assert "pat@example.com" in out
    assert "Odesa" in out
    assert "14.10.1992" in out


def test_main_contact_for_missing_contact_shows_error(monkeypatch, capsys, tmp_path):
    """Перевіряє помилку contact для неіснуючого контакту."""
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            "contact Ghost",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("src.scripts.contacts_bot.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert CONTACT_MESSAGES["NO_SUCH_CONTACT"] in out
    assert COMMAND_MESSAGES["GOOD_BYE"] in out


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
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів contact."""
    file_path = str(tmp_path / "address_book.pkl")
    lines = iter(
        [
            command_line,
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("src.scripts.contacts_bot.SERIALIZER_PATH", file_path)

    main()

    out = capsys.readouterr().out
    assert CONTACT_MESSAGES["INVALID_SYNTAX"] in out
    assert COMMAND_MESSAGES["GOOD_BYE"] in out
