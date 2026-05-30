from src.fields.email import Email
from src.fields.field import Field
import pytest


def test_email_is_subclass_of_field():
    """Перевіряє ієрархію класу Email.

    Дано:
        Класи ``Email`` та ``Field``.
    Коли:
        Перевіряється ієрархія класів.
    Тоді:
        ``Email`` є підкласом ``Field``.
    """
    assert issubclass(Email, Field)


@pytest.mark.parametrize(
    "email",
    [
        ("test@example.com"),
        ("test@example.com.ua"),
        ("test@example.com.ua.com"),
        ("test@example.com.ua.com.ua"),
        ("test@example.com.ua.com.ua.com"),
    ],
)
def test_email_valid(email):
    assert Email(email).validate()

@pytest.mark.parametrize(
    "email",
    [
        (""),
        ("укр@пошта.ком"),
        ("test@"),
        ("@example.com"),
        ("test@example"),
        ("test"),
    ],
)
def test_email_invalid(email):
    assert not Email(email).validate()