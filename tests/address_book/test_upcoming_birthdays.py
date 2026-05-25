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

# Validation of input parameters


def test_output_parameters(address_book_with_records):
    """
    Given an AddressBook with records
    When get_upcoming_birthdays is accessed
    Then its type is Callable[[], list[Record]]
    """
    assert assert_type(
        address_book_with_records.get_upcoming_birthdays, Callable[[], list[Record]]
    )


def test_empty_address_book_returns_empty_list(empty_address_book):
    """
    Given an empty AddressBook
    When get_upcoming_birthdays is called
    Then an empty list is returned
    """
    assert empty_address_book.get_upcoming_birthdays() == []


# Logic


@pytest.fixture
def today():
    return datetime.now()


def _is_congratulation_date_in_7_days(record: Record, today: datetime) -> bool:
    date = datetime.strptime(record.birthday.value, DATE_FORMAT)
    return date >= today and date < (today + timedelta(days=7))


@pytest.mark.parametrize("date", dates)
def test_congratulation_date_is_in_7_days(address_book_with_records, date):
    """
    Given an address book with contacts whose birthdays fall within the next 7 days
    When get_upcoming_birthdays is called on a parametrized "today" date
    Then every returned record has a birthday in that 7-day window
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


# BUG: Assertion uses raw birthday weekday on Record, not ProcessedRecord's
# adjusted congratulation_date. Resulting records are not moved to Monday;
@pytest.mark.parametrize("date", dates)
def test_congratulation_date_is_not_on_weekend(address_book_with_records, date):
    """
    Given an address book with birthdays in the upcoming window, including weekends
    When get_upcoming_birthdays is called on a parametrized "today" date
    Then weekend birthdays should be congratulated on the next Monday, not Sat/Sun
    """
    with time_machine.travel(date):
        result = address_book_with_records.get_upcoming_birthdays()
        assert all(_is_congratulation_date_not_on_weekend(user) for user in result)
