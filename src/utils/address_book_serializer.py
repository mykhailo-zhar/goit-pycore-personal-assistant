import pickle
from pathlib import Path
from typing import Callable

from src.address_book import AddressBook


class AddressBookSerializer:
    def __init__(
        self,
        file_path: str,
        send_error_message: Callable[[str], None] = lambda message: None,
    ):
        """
        Ініціалізує серіалізатор адресної книги.

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

    def serialize(self, address_book: AddressBook) -> None:
        """
        Зберігає адресну книгу у файл.

        Аргументи:
            address_book (AddressBook): Книга для збереження.
        """
        try:
            with open(self.file_path, "wb") as f:
                pickle.dump(address_book, f)
        except OSError:
            self.send_error_message(
                f"Warning: Failed to serialize address book to {self.file_path}"
            )

    def deserialize(self) -> AddressBook:
        """
        Завантажує адресну книгу з файлу.

        Повертає:
            AddressBook: Завантажена книга або порожня при помилці.
        """

        try:
            with open(self.file_path, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, OSError):
            self.send_error_message(
                f"Warning: Failed to deserialize address book from {self.file_path}"
            )
            return AddressBook()
