import builtins
from datetime import datetime

import pytest
import time_machine

from main import main
from src.commands.birthdays import BIRTHDAYS_MESSAGES
from src.utils.serializers.address_book import AddressBookSerializer


@pytest.fixture
def serializer(tmp_path):
    return AddressBookSerializer(str(tmp_path / "address_book.pkl"))


@time_machine.travel(datetime(2026, 5, 28))
def test_birthdays_shows_upcoming(monkeypatch, capsys, serializer):
    """Перевіряє виведення найближчих днів народження.

    Дано:
        Адресна книга з контактом Pat, чий день народження у найближчі 7 днів.
    Коли:
        Виконується ``birthdays 7``.
    Тоді:
        У виводі з'являється ім'я контакту та дата привітання.
    """
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-birthday Pat 02.06.1990",
            "birthdays 7",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert "Pat:" in out
    assert "02.06.2026" in out


@time_machine.travel(datetime(2026, 5, 28))
def test_birthdays_no_upcoming(monkeypatch, capsys, serializer):
    """Перевіряє повідомлення при відсутності найближчих днів народження.

    Дано:
        Адресна книга з контактом Pat, чий день народження поза вікном пошуку.
    Коли:
        Виконується ``birthdays 7``.
    Тоді:
        Виводиться повідомлення про відсутність найближчих днів народження.
    """
    lines = iter(
        [
            "add Pat 1234567890",
            "insert-birthday Pat 02.06.1990",
            "birthdays 0",
            "exit",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert BIRTHDAYS_MESSAGES["BIRTHDAYS_NO_UPCOMMING"] in out


def test_birthdays_empty_book(monkeypatch, capsys, serializer):
    """Перевіряє повідомлення для порожньої адресної книги.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується ``birthdays 7``.
    Тоді:
        Виводиться повідомлення про відсутність найближчих днів народження.
    """
    lines = iter(["birthdays 7", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert BIRTHDAYS_MESSAGES["BIRTHDAYS_NO_UPCOMMING"] in out


@pytest.mark.parametrize(
    "command_line",
    ["birthdays", "birthdays 7 14"],
)
def test_birthdays_invalid_syntax(monkeypatch, capsys, serializer, command_line):
    """Перевіряє синтаксичну помилку для невалідної кількості аргументів.

    Дано:
        Команда ``birthdays`` з неправильною арністю.
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
    assert BIRTHDAYS_MESSAGES["BIRTHDAYS_SYNTAX"] in out


def test_birthdays_invalid_days(monkeypatch, capsys, serializer):
    """Перевіряє помилку для невалідного значення днів.

    Дано:
        Порожня адресна книга.
    Коли:
        Виконується ``birthdays abc``.
    Тоді:
        Виводиться повідомлення про невалідну кількість днів.
    """
    lines = iter(["birthdays abc", "exit"])
    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr("main.SERIALIZER_PATH", serializer.file_path)
    main()

    out = capsys.readouterr().out
    assert BIRTHDAYS_MESSAGES["BIRTHDAYS_DAYS"] in out
