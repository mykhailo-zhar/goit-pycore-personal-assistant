import pickle
from pathlib import Path
from typing import Any, Callable, TypeVar

from .base import Serializer

T = TypeVar("T")


class PickleSerializer[T](Serializer):
    """
    Серіалізатор pickle.

    Аргументи:
        file_path (str): Шлях до файлу збереження.
        send_error_message (Callable[[str], None]): Функція для виводу попереджень.

    Винятки:
        FileNotFoundError: Якщо шлях вказує на директорію.
    """

    def __init__(
        self,
        file_path: str,
        send_error_message: Callable[[str], None] = lambda message: None,
    ):
        """
        Ініціалізує серіалізатор pickle.

        Аргументи:
            file_path (str): Шлях до файлу збереження.
            send_error_message (Callable[[str], None]): Функція для виводу попереджень.

        Винятки:
            FileNotFoundError: Якщо шлях вказує на директорію.
        """
        self.file_path = Path(file_path)
        self.send_error_message = send_error_message
        if self.file_path.is_dir():
            raise FileNotFoundError(f"Path {self.file_path} must not be a directory")

    def serialize(self, object: Any) -> T:
        with open(self.file_path, "wb") as f:
            pickle.dump(object, f)

    def deserialize(self) -> T:
        with open(self.file_path, "rb") as f:
            return pickle.load(f)
