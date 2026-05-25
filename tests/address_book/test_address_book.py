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
    """Перевіряє початковий стан нової адресної книги.

    Дано:
        Нова ``AddressBook``.
    Коли:
        Зчитується атрибут ``data``.
    Тоді:
        Це порожній словник.
    """
    assert address_book.data == {}


def test_address_book_add_record(address_book, record, valid_name):
    """Перевіряє додавання запису до книги.

    Дано:
        Порожня ``AddressBook`` і ``Record``.
    Коли:
        Викликається ``add_record``.
    Тоді:
        Запис зберігається за ключем імені контакту.

    Args:
        address_book: Порожня адресна книга.
        record: Запис контакту.
        valid_name: Ім'я контакту.
    """
    address_book.add_record(record)
    assert address_book.data == {valid_name: record}


def test_address_book_find_record(address_book, record, valid_name):
    """Перевіряє пошук наявного запису.

    Дано:
        ``AddressBook`` із доданим записом.
    Коли:
        Викликається ``find_record`` з іменем контакту.
    Тоді:
        Повертається той самий екземпляр ``Record``.

    Args:
        address_book: Книга з одним записом.
        record: Очікуваний запис.
        valid_name: Ім'я контакту.
    """
    address_book.add_record(record)
    assert address_book.find_record(valid_name) == record


def test_address_book_find_non_existent_record(address_book, valid_name):
    """Перевіряє пошук відсутнього запису.

    Дано:
        Порожня ``AddressBook``.
    Коли:
        Викликається ``find_record`` для неіснуючого імені.
    Тоді:
        Повертається ``None``.

    Args:
        address_book: Порожня адресна книга.
        valid_name: Ім'я, якого немає в книзі.
    """
    assert address_book.find_record(valid_name) is None


def test_address_book_remove_record(address_book, record, valid_name):
    """Перевіряє видалення наявного запису.

    Дано:
        ``AddressBook`` із записом.
    Коли:
        Викликається ``remove_record`` з іменем контакту.
    Тоді:
        Повертається ``True`` і запис більше не знаходиться.

    Args:
        address_book: Книга з одним записом.
        record: Запис для видалення.
        valid_name: Ім'я контакту.
    """
    address_book.add_record(record)
    assert address_book.remove_record(valid_name)
    assert address_book.find_record(valid_name) is None


def test_address_book_remove_non_existent_record(address_book, valid_name):
    """Перевіряє видалення відсутнього запису.

    Дано:
        Порожня ``AddressBook``.
    Коли:
        Викликається ``remove_record`` для неіснуючого імені.
    Тоді:
        Повертається ``False``.

    Args:
        address_book: Порожня адресна книга.
        valid_name: Ім'я, якого немає в книзі.
    """
    assert not address_book.remove_record(valid_name)
