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
        Initialize the address book serializer.

        Args:
            file_path (str): The path to the file to serialize the address book to.
            send_error_message (Callable[[str], None]): The function to send error messages.
        Raises:
            FileNotFoundError: If the file path is not a file or does not exist.
        """
        self.file_path = Path(file_path)
        self.send_error_message = send_error_message
        if self.file_path.is_dir():
            raise FileNotFoundError(f"Path {self.file_path} must not be a directory")

    def serialize(self, address_book: AddressBook) -> None:
        """
        Serialize the address book to the file.

        Args:
            address_book (AddressBook): The address book to serialize.

        Returns:
            str: The serialized address book.
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
        Deserialize the address book from the file.

        Returns:
            AddressBook: The deserialized address book.
        """

        try:
            with open(self.file_path, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, OSError):
            self.send_error_message(
                f"Warning: Failed to deserialize address book from {self.file_path}"
            )
            return AddressBook()
