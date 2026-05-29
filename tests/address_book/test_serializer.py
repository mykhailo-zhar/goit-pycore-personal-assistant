from pathlib import Path
from typing import Callable, get_type_hints

import pytest

from src.address_book import AddressBook
from src.record import Record
from src.utils.serializers.address_book import AddressBookSerializer


@pytest.fixture
def address_book():
    address_book = AddressBook()
    john_doe = Record("JohnDoe")
    john_doe.add_phone("1234567890")
    john_doe.add_phone("0987654321")
    john_doe.add_birthday("01.01.1990")
    address_book.add_record(john_doe)
    return address_book


@pytest.fixture
def serializer(tmp_path):
    file_path = tmp_path / "addressbook.pkl"
    return AddressBookSerializer(file_path, lambda message: print(message))


def test_serializer_without_file_path():
    """Перевіряє анотації типів конструктора серіалізатора.

    Дано:
        Клас ``AddressBookSerializer``.
    Коли:
        Переглядаються type hints ``__init__``.
    Тоді:
        ``file_path`` — ``str``, ``send_error_message`` — ``Callable[[str], None]``.
    """
    hints = get_type_hints(AddressBookSerializer.__init__)
    assert hints["file_path"] is str
    assert hints["send_error_message"] is Callable[[str], None]


def test_serializer_constructor_checks_whether_file_path_is_a_directory(tmp_path):
    """Перевіряє заборону шляху до директорії.

    Дано:
        Шлях до існуючої директорії.
    Коли:
        Створюється ``AddressBookSerializer`` з цим шляхом.
    Тоді:
        Виникає ``FileNotFoundError``.

    Args:
        tmp_path: Тимчасова директорія pytest.
    """
    with pytest.raises(FileNotFoundError):
        AddressBookSerializer(tmp_path.absolute())


def test_serialize_address_book(address_book, serializer):
    """Перевіряє round-trip серіалізації книги.

    Дано:
        Заповнена ``AddressBook`` і серіалізатор з файлом.
    Коли:
        Виконуються ``serialize`` і ``deserialize``.
    Тоді:
        Відновлена книга містить ті самі дані контакту.

    Args:
        address_book: Книга з контактом JohnDoe.
        serializer: Серіалізатор у ``tmp_path``.
    """
    serializer.serialize(address_book)
    deserialized_address_book = serializer.deserialize()
    assert len(deserialized_address_book.data) == len(address_book.data)

    record = deserialized_address_book.find_record("JohnDoe")
    assert record is not None
    assert record.name.value == "JohnDoe"
    assert len(record.phones) == 2
    assert record.phones[0].value == "1234567890"
    assert record.phones[1].value == "0987654321"
    assert record.birthday.value == "01.01.1990"


def test_deserialize_address_book_with_empty_file(serializer, capsys):
    """Перевіряє десеріалізацію при відсутньому файлі.

    Дано:
        Серіалізатор без існуючого pickle-файлу.
    Коли:
        Викликається ``deserialize``.
    Тоді:
        Повертається порожня ``AddressBook`` і виводиться попередження.

    Args:
        serializer: Серіалізатор у ``tmp_path``.
        capsys: Захоплення stdout pytest.
    """
    deserialized_address_book = serializer.deserialize()
    out = capsys.readouterr().out
    assert len(deserialized_address_book.data) == 0
    assert "Failed to deserialize address book from" in out


def test_deserialize_address_book_with_permissions_(serializer, capsys):
    """Перевіряє десеріалізацію при відсутності прав на читання.

    Дано:
        Файл серіалізатора існує, але недоступний для читання (chmod 0).
    Коли:
        Викликається ``deserialize``.
    Тоді:
        Повертається порожня ``AddressBook`` і виводиться попередження.

    Args:
        serializer: Серіалізатор із файлом.
        capsys: Захоплення stdout pytest.
    """
    file = Path(serializer.file_path)
    file.write_text("test", encoding="utf-8")
    file.chmod(0o000)
    deserialized_address_book = serializer.deserialize()
    out = capsys.readouterr().out
    assert len(deserialized_address_book.data) == 0
    assert "Failed to deserialize address book from" in out


def test_serialize_address_book_with_permissions_(serializer, capsys):
    """Перевіряє серіалізацію при відсутності прав на запис.

    Дано:
        Файл існує, але недоступний для запису (chmod 0).
    Коли:
        Викликається ``serialize`` з ``AddressBook``.
    Тоді:
        Виводиться попередження, виняток не виникає.

    Args:
        serializer: Серіалізатор із файлом.
        capsys: Захоплення stdout pytest.
    """
    file = Path(serializer.file_path)
    file.write_text("test", encoding="utf-8")
    file.chmod(0o000)
    serializer.serialize(AddressBook())
    out = capsys.readouterr().out
    assert "Failed to serialize address book to" in out
