from src.note import Note

NOTE_BOOK_ERRORS = {
    "NOTE_NOT_FOUND": "Note not found",
    "NOTE_ALREADY_EXISTS": "Note already exists",
}


class NoteBook:
    def __init__(self):
        """Ініціалізує книгу нотаток."""
        self.data: dict[str, Note] = {}

    def add_note(self, note: Note):
        """
        Додає нотатку до колекції.

        Аргументи:
            note (Note): Нотатка для додавання.

        Винятки:
            KeyError: Якщо нотатка з таким заголовком вже існує.
        """
        title = note.title.value
        if title in self.data:
            raise KeyError(NOTE_BOOK_ERRORS["NOTE_ALREADY_EXISTS"])
        self.data[title] = note

    def find_note(self, title: str) -> Note | None:
        """
        Шукає нотатку за заголовком.

        Аргументи:
            title (str): Заголовок нотатки.

        Повертає:
            Note | None: Нотатка, якщо знайдено, інакше None.
        """
        return self.data.get(title)

    def change_title(self, old_title: str, new_title: str):
        """
        Змінює заголовок нотатки.

        Аргументи:
            old_title (str): Поточний заголовок.
            new_title (str): Новий заголовок.

        Винятки:
            KeyError: Якщо нотатку не знайдено або новий заголовок зайнятий.
            ValueError: Якщо новий заголовок невалідний.
        """
        note = self.find_note(old_title)
        if note is None:
            raise KeyError(NOTE_BOOK_ERRORS["NOTE_NOT_FOUND"])

        if old_title != new_title and self.find_note(new_title) is not None:
            raise KeyError(NOTE_BOOK_ERRORS["NOTE_ALREADY_EXISTS"])

        note.edit_title(new_title)

        if old_title != new_title:
            del self.data[old_title]
            self.data[new_title] = note

    def remove_note(self, title: str) -> bool:
        """
        Видаляє нотатку з колекції.

        Аргументи:
            title (str): Заголовок нотатки.

        Повертає:
            bool: True, якщо нотатку видалено, інакше False.
        """
        return self.data.pop(title, None) is not None
