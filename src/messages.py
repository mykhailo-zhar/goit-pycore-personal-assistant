# src.scripts.contacts_bot.py messages
COMMAND_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "CONTACT_ADDED": "Contact added.",
    "CONTACT_UPDATED": "Contact updated.",
    "BIRTHDAY_ADDED": "Birthday added. Replacing {old_birthday} with {new_birthday} for {name}",
    "NO_BIRTHDAY_SET": "No birthday set for {name}",
    "BIRTHDAY_SHOWED": "Birthday for {name} is {birthday}",
    "UPCOMING_BIRTHDAYS": "Upcoming birthdays:\n{birthdays}",
    "NO_SUCH_USER": "No such user",
    "PLEASE_CHANGE_USER": "Please change the user",
    "GOOD_BYE": "Good bye!",
    "HELLO": "How can I help you?",
    "PHONE_CHANGED": "Phone was changed",
    "PHONE_CHANGE_SYNTAX": "Syntax: change-phone <name> <old phone> <new phone>",
    "BIRTHDAYS_SYNTAX": "Syntax: birthdays <days>",
    "BIRTHDAYS_DAYS": "Days must be a non-negative integer.",
    "BIRTHDAYS_NO_UPCOMMING": "No upcoming birthdays.",
    "BIRTHDAYS_FORMAT": "%d.%m.%Y",
    "PHONES_TRUNCATED": "Phones updated for {name}: {phone}",
    "TRUNCATE_SYNTAX": "Syntax: truncate <name> <new_phone>",
    }
# src.commands.add_note.py messages
ADD_NOTE_MESSAGES = {
    "INVALID_SYNTAX": "Add note command should have the following syntax: add-note <title>",
    "NOTE_ALREADY_PRESENT": "Note is already present.",
    "NOTE_ADDED": "Note added: {title}",
    }

# src.commands.add_tag.py messages
ADD_TAG_MESSAGES = {
    "INVALID_SYNTAX": "Add tag command should have the following syntax: add-tag <title> <tag>",
    "NO_SUCH_NOTE": "There is no such note",
    "TAG_ALREADY_EXISTS": "There is already such tag",
    "TAG_ADDED": "Tag added",
    }
