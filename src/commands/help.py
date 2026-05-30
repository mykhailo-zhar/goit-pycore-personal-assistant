from src.address_book import AddressBook
from src.decorators.input_error import input_error


@input_error
def help(_: AddressBook, arguments: list[str]) -> str:
    """
    Показує довідку по командам.

    Аргументи:
        None

    Повертає:
        str: Довідка по командам.
    """
    return """USAGE: 
  [command] [arguments]

AVAILABLE COMMANDS:

  General
    hello                                    Greet the user.
    all                                      Show all contacts.
    exit, close                              Exit the program.

  Contacts
    add <name> <phone>                       Add a contact or a phone number to an existing contact.
    update <name> <phone>                    Update a contact's phone number(s).
    remove <name>                            Remove a contact.
    phone <name>                             Show a contact's phone number(s).
    insert-address <name> <address>          Insert an address for a contact.

  Birthdays
    add-birthday <name> <birthday>           Add a birthday for a contact (format: DD.MM.YYYY).
    show-birthday <name>                     Show a contact's birthday.
    birthdays <days>                         Show upcoming birthdays within the next specified number of days.

  Notes
    add-note <title> <text>                  Add a note with the given title and text.
    insert-text <title> <text>               Insert text into an existing note.
    change-title <old_title> <new_title>     Change the title of an existing note.
    note <title>                             Show the text of a note with the given title.

  Tags
    add-tag <title> <tag>                    Add a tag to a note.
    remove-tag <title> <tag>                 Remove a tag from a note.
    tag <tag>                                Show notes with the given tag.

EXAMPLES:
  $ add John 1234567890
  $ add-birthday Jane 25.12.1990
  $ add-note \"Shopping\" "Milk, Bread, Eggs"""
