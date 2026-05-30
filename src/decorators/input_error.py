from functools import wraps


def input_error(func):
    """Декоратор для обробки помилок введення."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Викликає обгорнуту функцію та перехоплює помилки введення.

        Аргументи:
            *args: Позиційні аргументи для обгорнутої функції.
            **kwargs: Іменовані аргументи для обгорнутої функції.

        Повертає:
            Any: Результат функції або рядок-повідомлення про помилку.
        """
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError, KeyError) as e:
            return f"[red]Error: {e}[/red]"

    return wrapper
