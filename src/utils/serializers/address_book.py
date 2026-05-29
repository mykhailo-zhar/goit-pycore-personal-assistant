from src.address_book import AddressBook
from src.utils.serializers.pickle import PickleSerializer


class AddressBookSerializer(PickleSerializer[AddressBook]):
    def serialize(self, address_book: AddressBook) -> None:
        """
        Зберігає адресну книгу у файл.

        Аргументи:
            address_book (AddressBook): Книга для збереження.
        """
        try:
            super().serialize(address_book)
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
            return super().deserialize()
        except (FileNotFoundError, OSError):
            self.send_error_message(
                f"Warning: Failed to deserialize address book from {self.file_path}"
            )
            return AddressBook()
