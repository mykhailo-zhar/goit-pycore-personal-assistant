import pytest

from src.address_book import AddressBook
from src.record import Record


@pytest.fixture
def valid_name():
    return "John"


@pytest.fixture
def record(valid_name):
    return Record(valid_name)


def test_address_book_init():
    address_book = AddressBook()
    assert address_book.data == {}


def test_address_book_add_record(record, valid_name):
    address_book = AddressBook()
    address_book.add_record(record)
    assert address_book.data == {valid_name: record}


def test_address_book_find_record(record, valid_name):
    address_book = AddressBook()
    address_book.add_record(record)
    assert address_book.find_record(valid_name) == record


def test_address_book_find_non_existent_record(valid_name):
    address_book = AddressBook()
    assert address_book.find_record(valid_name) is None


def test_address_book_remove_record(record, valid_name):
    address_book = AddressBook()
    address_book.add_record(record)
    assert address_book.remove_record(valid_name)
    assert address_book.find_record(valid_name) is None


def test_address_book_remove_non_existent_record(valid_name):
    address_book = AddressBook()
    assert not address_book.remove_record(valid_name)
