from functools import wraps
from typing import Any


def serializes(func, object: Any, serializer=None):
    """
    Декоратор для збереження адресної книги після команди.

    Аргументи:
        func (Callable): Функція-обробник.
        object (Any): Об'єкт для серіалізації.
        serializer (AddressBookSerializer | None): Серіалізатор.

    Повертає:
        Callable: Обгорнута функція.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if serializer:
            serializer.serialize(object)
        return result

    return wrapper
