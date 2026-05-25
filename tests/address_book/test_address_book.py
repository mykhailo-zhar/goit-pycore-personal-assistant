import pytest

from src.address_book import AddressBook
from src.record import Record


@pytest.fixture
def valid_name():
    return "John"


@pytest.fixture
def record(valid_name):
    return Record(valid_name)


@pytest.fixture
def address_book():
    return AddressBook()


def test_address_book_init(address_book):
    """
    Given a new AddressBook
    When the data attribute is read
    Then it is an empty dict
    """
    assert address_book.data == {}


def test_address_book_add_record(address_book, record, valid_name):
    """
    Given an empty AddressBook and a Record
    When add_record is called
    Then the record is stored under the contact name key
    """
    address_book.add_record(record)
    assert address_book.data == {valid_name: record}


def test_address_book_find_record(address_book, record, valid_name):
    """
    Given an AddressBook containing a record
    When find_record is called with that contact name
    Then the same Record instance is returned
    """
    address_book.add_record(record)
    assert address_book.find_record(valid_name) == record


def test_address_book_find_non_existent_record(address_book, valid_name):
    """
    Given an empty AddressBook
    When find_record is called with a name that was never added
    Then None is returned
    """
    assert address_book.find_record(valid_name) is None


def test_address_book_remove_record(address_book, record, valid_name):
    """
    Given an AddressBook containing a record
    When remove_record is called with that name
    Then it returns True and the record is no longer findable
    """
    address_book.add_record(record)
    assert address_book.remove_record(valid_name)
    assert address_book.find_record(valid_name) is None


def test_address_book_remove_non_existent_record(address_book, valid_name):
    """
    Given an empty AddressBook
    When remove_record is called with a missing name
    Then it returns False
    """
    assert not address_book.remove_record(valid_name)
