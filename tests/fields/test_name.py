import pytest

from src.fields.field import Field
from src.fields.name import Name


def test_name_is_subclass_of_field():
    """Перевіряє ієрархію класу Name.

    Дано:
        Класи ``Name`` та ``Field``.
    Коли:
        Перевіряється ієрархія класів.
    Тоді:
        ``Name`` є підкласом ``Field``.
    """
    assert issubclass(Name, Field)


def test_name_init():
    """Перевіряє ініціалізацію імені.

    Дано:
        Рядок ``"John Doe"``.
    Коли:
        Створюється екземпляр ``Name``.
    Тоді:
        ``value`` дорівнює ``"John Doe"``.
    """
    name = Name("John Doe")
    assert name.value == "John Doe"


def test_name_str():
    """Перевіряє рядкове подання імені.

    Дано:
        ``Name`` зі значенням ``"John Doe"``.
    Коли:
        Викликається ``str()`` на імені.
    Тоді:
        Результат — ``"John Doe"``.
    """
    name = Name("John Doe")
    assert str(name) == "John Doe"


@pytest.mark.parametrize(
    "name, is_valid",
    [
        (10, False),
        ("", False),
        (None, False),
        ("John Doe", False),
        ("John Doe1", False),
        ("JohnDoe1", True),
        ("John", True),
    ],
)
def test_name_validate(name, is_valid):
    """Перевіряє валідацію імені для різних значень.

    Дано:
        Параметризоване кандидат-значення імені.
    Коли:
        Викликається ``Name(name).validate()``.
    Тоді:
        Результат відповідає очікуваній валідності.

    Args:
        name: Значення для перевірки.
        is_valid: Очікуваний результат валідації.
    """
    assert Name(name).validate() == is_valid
