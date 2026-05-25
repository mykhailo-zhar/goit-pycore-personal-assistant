from collections.abc import Callable
from typing import assert_type

import pytest

from src.fields.field import Field


@pytest.fixture
def field():
    return Field("test")


def test_field_init(field):
    """
    Given a Field instance with value "test"
    When the value attribute is read
    Then it equals "test"
    """
    assert field.value == "test"


def test_field_str(field):
    """
    Given a Field instance with value "test"
    When str() is called on the field
    Then the result is "test"
    """
    assert str(field) == "test"


def test_field_has_validate(field):
    """
    Given a Field instance
    When validate is accessed
    Then it is a callable that takes no arguments and returns bool
    """
    assert assert_type(field.validate, Callable[[], bool])
