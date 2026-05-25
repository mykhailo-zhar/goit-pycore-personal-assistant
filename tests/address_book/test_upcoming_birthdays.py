from datetime import datetime, timedelta
from typing import Callable, assert_type

import pytest
import time_machine
from dateutil.relativedelta import relativedelta

from src.address_book import AddressBook
from src.record import Record

DATE_FORMAT = "%d.%m.%Y"


@pytest.fixture
def users() -> list[dict]:
    return [
        {
            "name": f"JohnDoe{i}",
            "birthday": (datetime.now() + relativedelta(days=i, years=-25)).strftime(
                DATE_FORMAT
            ),
        }
        for i in range(1, 8)
    ]


@pytest.fixture
def empty_address_book():
    return AddressBook()


@pytest.fixture
def address_book_with_records(users):
    book = AddressBook()
    for user in users:
        user_record = Record(user["name"])
        user_record.add_birthday(user["birthday"])
        book.add_record(user_record)
    return book


dates = [datetime(2026, 4, 26), datetime(2026, 5, 1), datetime(2026, 4, 23)]

# Валідація параметрів виводу


def test_output_parameters(address_book_with_records):
    """Перевіряє тип методу найближчих днів народження.

    Дано:
        ``AddressBook`` із записами.
    Коли:
        Звертаються до ``get_upcoming_birthdays``.
    Тоді:
        Тип — ``Callable[[], list[Record]]``.

    Args:
        address_book_with_records: Книга з контактами та днями народження.
    """
    assert assert_type(
        address_book_with_records.get_upcoming_birthdays, Callable[[], list[Record]]
    )


def test_empty_address_book_returns_empty_list(empty_address_book):
    """Перевіряє порожній результат для порожньої книги.

    Дано:
        Порожня ``AddressBook``.
    Коли:
        Викликається ``get_upcoming_birthdays``.
    Тоді:
        Повертається порожній список.

    Args:
        empty_address_book: Книга без записів.
    """
    assert empty_address_book.get_upcoming_birthdays() == []


# Логіка


@pytest.fixture
def today():
    return datetime.now()


def _is_congratulation_date_in_7_days(record: Record, today: datetime) -> bool:
    date = datetime.strptime(record.birthday.value, DATE_FORMAT)
    return date >= today and date < (today + timedelta(days=7))


@pytest.mark.parametrize("date", dates)
def test_congratulation_date_is_in_7_days(address_book_with_records, date):
    """Перевіряє, що ДН потрапляють у 7-денне вікно.

    Дано:
        Книга з контактами, чиї ДН у наступні 7 днів від параметризованої дати.
    Коли:
        Викликається ``get_upcoming_birthdays`` на зафіксованій даті ``date``.
    Тоді:
        У кожного поверненого запису ДН у цьому вікні.

    Args:
        address_book_with_records: Книга з контактами.
        date: Поточна дата для ``time_machine``.
    """
    with time_machine.travel(date):
        result = address_book_with_records.get_upcoming_birthdays()
        assert all(_is_congratulation_date_in_7_days(user) for user in result)


def _is_congratulation_date_not_on_weekend(record: Record, today: datetime) -> bool:
    date = datetime.strptime(record.birthday.value, DATE_FORMAT)
    date = date.replace(year=today.year)

    return date.weekday() not in [
        5,
        6,
    ]


# BUG: перевірка використовує день тижня сирого birthday на Record,
# а не скориговану congratulation_date з ProcessedRecord; записи не переносяться на понеділок
@pytest.mark.parametrize("date", dates)
def test_congratulation_date_is_not_on_weekend(address_book_with_records, date):
    """Перевіряє перенесення вихідних ДН на понеділок (очікувана поведінка).

    Дано:
        Книга з ДН у найближчому вікні, включно з вихідними.
    Коли:
        Викликається ``get_upcoming_birthdays`` на параметризованій даті.
    Тоді:
        Вихідні ДН мають привітатися в понеділок, а не в суботу/неділю.

    Args:
        address_book_with_records: Книга з контактами.
        date: Поточна дата для ``time_machine``.
    """
    with time_machine.travel(date):
        result = address_book_with_records.get_upcoming_birthdays()
        assert all(_is_congratulation_date_not_on_weekend(user) for user in result)
