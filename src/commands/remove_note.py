from src.note import Note
from src.note_book import NoteBook
from src.utils.decorators.input_error import input_error

ADD_NOTE_MESSAGES = {
    "INVALID_SYNTAX": "Add note command should have the following syntax: add-note <title>",
    "NOTE_ALREADY_PRESENT": "Note is already present.",
    "NOTE_ADDED": "Note added: {title}",
    }


@input_error
def remove_note(note_book: NoteBook, arguments: list[str]) -> bool:
    """
        Видаляє нотатку за заголовком.

        Аргументи:
            title (str): Заголовок нотатки для видалення.

        Повертає:
            bool: True, якщо нотатку знайдено і видалено, інакше False.
        """
    if len(arguments) != 1:
        raise ValueError(ADD_NOTE_MESSAGES["INVALID_SYNTAX"])
    title = arguments[0]

    if note_book.find_note(title):
        del note_book.data[title]
        return True

    return False
