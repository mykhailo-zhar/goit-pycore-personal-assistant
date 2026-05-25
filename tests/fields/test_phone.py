import pytest

from src.fields.field import Field
from src.fields.phone import Phone


def test_phone_is_subclass_of_field():
    """Перевіряє ієрархію класу Phone.

    Дано:
        Класи ``Phone`` та ``Field``.
    Коли:
        Перевіряється ієрархія класів.
    Тоді:
        ``Phone`` є підкласом ``Field``.
    """
    assert issubclass(Phone, Field)


@pytest.fixture
def valid_phone():
    return Phone("1234567890")


def test_phone_init(valid_phone):
    """Перевіряє збереження номера телефону.

    Дано:
        ``Phone``, створений з ``"1234567890"``.
    Коли:
        Зчитується атрибут ``value``.
    Тоді:
        Значення дорівнює ``"1234567890"``.

    Args:
        valid_phone: Валідний телефон.
    """
    assert valid_phone.value == "1234567890"


def test_phone_str(valid_phone):
    """Перевіряє рядкове подання телефону.

    Дано:
        ``Phone`` зі значенням ``"1234567890"``.
    Коли:
        Викликається ``str()`` на телефоні.
    Тоді:
        Результат — ``"1234567890"``.

    Args:
        valid_phone: Валідний телефон.
    """
    assert str(valid_phone) == "1234567890"


@pytest.mark.parametrize(
    "phone, is_valid",
    [
        ("1234567", False),
        ("1234567890", True),
        ("12345678901", False),
        ("123456789012", False),
        ("123456789a", False),
    ],
)
def test_phone_validate(phone, is_valid):
    """Перевіряє валідацію номера для різних рядків.

    Дано:
        Параметризований рядок телефону.
    Коли:
        Викликається ``Phone(phone).validate()``.
    Тоді:
        Результат відповідає очікуваній валідності.

    Args:
        phone: Рядок номера.
        is_valid: Очікуваний результат валідації.
    """
    phone = Phone(phone)
    assert phone.validate() == is_valid
