from collections.abc import Callable
from typing import assert_type

import pytest

from src.fields.field import Field


@pytest.fixture
def field():
    return Field("test")


def test_field_init(field):
    """Перевіряє збереження значення поля.

    Дано:
        Екземпляр ``Field`` зі значенням ``"test"``.
    Коли:
        Зчитується атрибут ``value``.
    Тоді:
        Значення дорівнює ``"test"``.

    Args:
        field: Поле з тестовим значенням.
    """
    assert field.value == "test"


def test_field_str(field):
    """Перевіряє рядкове подання поля.

    Дано:
        Екземпляр ``Field`` зі значенням ``"test"``.
    Коли:
        Викликається ``str()`` на полі.
    Тоді:
        Результат — ``"test"``.

    Args:
        field: Поле з тестовим значенням.
    """
    assert str(field) == "test"


def test_field_has_validate(field):
    """Перевіряє наявність методу validate.

    Дано:
        Екземпляр ``Field``.
    Коли:
        Звертаються до ``validate``.
    Тоді:
        Це викликабельний без аргументів, що повертає ``bool``.

    Args:
        field: Базове поле.
    """
    assert assert_type(field.validate, Callable[[], bool])
