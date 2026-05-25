import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_contact
from tests.contacts_bot.shared import INVALID_PHONE_12, RECORD_ERRORS


def test_add_contact_inserts_and_message(empty_address_book, valid_phone):
    assert (
        add_contact(empty_address_book, ["Zoe", valid_phone])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    assert len(empty_address_book.data) == 1


def test_add_contact_duplicate_phones(empty_address_book, valid_phone):
    assert (
        add_contact(empty_address_book, ["Zoe", valid_phone])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    assert (
        add_contact(empty_address_book, ["Zoe", valid_phone])
        == RECORD_ERRORS["PHONE_ALREADY_EXISTS"]
    )
    assert len(empty_address_book.data) == 1


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["bad"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        (["bad", "1234567890", "1234567890"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        (["bad", "name", INVALID_PHONE_12], COMMAND_MESSAGES["INVALID_COMMAND"]),
        (["bad name", "12345678901"], RECORD_ERRORS["NAME_NOT_VALID"]),
        (["Good", "+1234567890123456"], RECORD_ERRORS["PHONE_NOT_VALID"]),
    ],
)
def test_add_contact_invalid_name_or_phone(empty_address_book, arguments, expected):
    assert add_contact(empty_address_book, arguments) == expected
    assert len(empty_address_book.data) == 0


@pytest.fixture
def add_contact_fixture(valid_phone):
    return ["JohnDoe", valid_phone]


@pytest.mark.parametrize("add_contact_fixture", [i for i in range(10)], indirect=True)
def test_add_valid_name_and_phone(empty_address_book, add_contact_fixture):
    assert (
        add_contact(empty_address_book, add_contact_fixture)
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    assert len(empty_address_book.data) == 1
    assert len(empty_address_book.data["JohnDoe"].phones) == 1


def test_add_multiple_phones(empty_address_book, valid_phone_generator):
    valid_phones = [valid_phone_generator() for _ in range(3)]
    for phone in valid_phones:
        assert (
            add_contact(empty_address_book, ["JohnDoe", phone])
            == COMMAND_MESSAGES["CONTACT_ADDED"]
        )
    assert len(empty_address_book.data) == 1
    assert all(
        phone.value in valid_phones
        for phone in empty_address_book.data["JohnDoe"].phones
    )
