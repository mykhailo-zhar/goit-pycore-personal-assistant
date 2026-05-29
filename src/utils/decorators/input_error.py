from functools import wraps


def input_error(func):
    """Декоратор для обробки помилок введення."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError, KeyError) as e:
            return str(e)

    return wrapper
