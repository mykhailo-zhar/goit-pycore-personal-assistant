from src.scripts.contacts_bot import COMMAND_MESSAGES, update_contact
from tests.contacts_bot.shared import RECORD_ERRORS


def test_change_contact_updates(book_with_contact, valid_phone):
    assert (
        update_contact(book_with_contact, ["JohnDoe", valid_phone])
        == COMMAND_MESSAGES["CONTACT_UPDATED"]
    )
    assert any(
        phone.value == valid_phone for phone in book_with_contact.data["JohnDoe"].phones
    )


def test_change_contact_no_such_user(empty_address_book, valid_phone):
    assert (
        update_contact(empty_address_book, ["Nobody", valid_phone])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )
    assert len(empty_address_book.data) == 0


def test_change_contact_invalid_credentials(book_with_contact, valid_phone):
    assert (
        update_contact(book_with_contact, ["JohnDoe", "abcdefghijkl"])
        == RECORD_ERRORS["PHONE_NOT_VALID"]
    )
    assert any(
        phone.value == valid_phone for phone in book_with_contact.data["JohnDoe"].phones
    )


def test_change_contact_with_multiple_phones_is_not_allowed(
    book_with_contact, valid_phone_generator
):
    valid_phones = [valid_phone_generator() for _ in range(3)]
    assert (
        update_contact(book_with_contact, ["JohnDoe", *valid_phones])
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )
