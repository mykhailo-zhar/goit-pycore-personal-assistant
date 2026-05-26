import pytest

from src.fields.birthday import Birthday
from src.fields.field import Field


def test_birthday_is_subclass_of_field():
    """Перевіряє ієрархію класу Birthday.

    Дано:
        Класи ``Birthday`` та ``Field``.
    Коли:
        Перевіряється ієрархія класів.
    Тоді:
        ``Birthday`` є підкласом ``Field``.
    """
    assert issubclass(Birthday, Field)


@pytest.fixture
def valid_birthday_str():
    return "10.01.1990"


@pytest.fixture
def valid_birthday(valid_birthday_str):
    return Birthday(valid_birthday_str)


def test_birthday_init(valid_birthday, valid_birthday_str):
    """Перевіряє збереження дати народження.

    Дано:
        ``Birthday`` з валідним рядком DD.MM.YYYY.
    Коли:
        Зчитується атрибут ``value``.
    Тоді:
        Значення збігається з вхідним рядком.

    Args:
        valid_birthday: Екземпляр дня народження.
        valid_birthday_str: Очікуваний рядок дати.
    """
    assert valid_birthday.value == valid_birthday_str


def test_birthday_str(valid_birthday, valid_birthday_str):
    """Перевіряє рядкове подання дня народження.

    Дано:
        ``Birthday`` з валідним рядком дати.
    Коли:
        Викликається ``str()`` на полі.
    Тоді:
        Результат дорівнює збереженому значенню.

    Args:
        valid_birthday: Екземпляр дня народження.
        valid_birthday_str: Очікуваний рядок.
    """
    assert str(valid_birthday) == valid_birthday_str


def test_birthday_validate(valid_birthday):
    """Перевіряє валідацію коректної дати.

    Дано:
        ``Birthday`` зі значенням ``"10.01.1990"``.
    Коли:
        Викликається ``validate()``.
    Тоді:
        Повертається ``True``.

    Args:
        valid_birthday: Валідний день народження.
    """
    assert valid_birthday.validate()


def test_birthday_29_february_2000_validate_returns_true():
    """Перевіряє, що 29 лютого 2000 року є валідною датою народження.

    Дано:
        ``Birthday`` зі значенням ``"29.02.2000"``.
    Коли:
        Викликається ``validate()``.
    Тоді:
        Метод повертає ``True``.
    """
    birthday = Birthday("29.02.2000")

    assert birthday.validate()


@pytest.mark.parametrize(
    "birthday",
    [
        "29.02.2001",
        "29.02.1999",
        "29.02.1900",
    ],
)
def test_birthday_29_february_non_leap_year_validate_returns_false(birthday):
    """Перевіряє, що 29 лютого у невисокосний рік є невалідною датою.

    Дано:
        ``Birthday`` зі значенням 29 лютого у невисокосний рік.
    Коли:
        Викликається ``validate()``.
    Тоді:
        Метод повертає ``False``.
    """
    assert not Birthday(birthday).validate()


@pytest.mark.parametrize(
    "birthday",
    [
        "1990-01-01",
        "10/01/1990",
        "10.13.1990",
        "test",
        None,
        10,
        10.0,
        True,
        False,
        ["10.01.1990"],
        {"10.01.1990": "10.01.1990"},
        {"10.01.1990"},
    ],
)
def test_birthday_validate_invalid(birthday):
    """Перевіряє відхилення невалідних значень дати.

    Дано:
        Параметризоване невалідне значення дня народження.
    Коли:
        Викликається ``Birthday(birthday).validate()``.
    Тоді:
        Повертається ``False``.

    Args:
        birthday: Невалідне значення для перевірки.
    """
    assert not Birthday(birthday).validate()
