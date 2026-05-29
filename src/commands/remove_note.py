from src.note import Note
from src.note_book import NoteBook
from src.utils.decorators.input_error import input_error

REMOVE_NOTE_MESSAGES = {
    "INVALID_SYNTAX": "Remove note command should have the following syntax: remove-note <title>",
    "NOTE_ALREADY_DELETED": "Note is already deleted.",
    "NOTE_NOT_FOUND": "Note not found.",
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
        raise ValueError(REMOVE_NOTE_MESSAGES["INVALID_SYNTAX"])
    title = arguments[0]

    if note_book.find_note(title):
        del note_book.data[title]
        print(REMOVE_NOTE_MESSAGES["NOTE_ALREADY_DELETED"])
        return True

    print(REMOVE_NOTE_MESSAGES["NOTE_NOT_FOUND"])
    return False
