from src.note_book import NoteBook
from src.utils.serializers.pickle import PickleSerializer


class NoteBookSerializer(PickleSerializer[NoteBook]):
    def serialize(self, object: NoteBook) -> None:
        """
        Зберігає книгу нотаток у файл.

        Аргументи:
            object (NoteBook): Книга для збереження.
        """
        try:
            super().serialize(object)
        except OSError:
            self.send_error_message(
                f"Warning: Failed to serialize note book to {self.file_path}"
            )

    def deserialize(self) -> NoteBook:
        """
        Завантажує книгу нотаток з файлу.

        Повертає:
            NoteBook: Завантажена книга або порожня при помилці.
        """

        try:
            return super().deserialize()
        except (FileNotFoundError, OSError):
            self.send_error_message(
                f"Warning: Failed to deserialize note book from {self.file_path}"
            )
            return NoteBook()
