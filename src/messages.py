from src.record import ADDRESS_NOT_VALID_ERROR

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

# src.command.change_title.py messages
CHANGE_TITLE_MESSAGES = {
    "INVALID_SYNTAX": "Change title command should have the following syntax: change-title <old_title> <new_title>",
    "NO_SUCH_NOTE": "No such note",
    "NOTE_ALREADY_EXISTS": "Note already exists",
    "TITLE_CHANGED": "Title was changed",
    }
# src.command.find_by_tag.py messages
FIND_BY_TAG_MESSAGES = {
    "INVALID_SYNTAX": "Tag command should have the following syntax: tag <tag> <order>",
    "INVALID_ORDER": "There are only ascending and descending order.",
    "NO_NOTES": "There are no notes,",
    }
# src.command.find_by_tag.py messages
INSERT_ADDRESS_MESSAGES = {
    "INVALID_SYNTAX": "Insert address command should have the following syntax: insert-address <name> <address>",
    "ADDRESS_ADDED": "Address added.",
    "ADDRESS_REPLACED": "Replacing {old_address} with {new_address} for {name}",
    "NO_SUCH_CONTACT": "No such contact.",
    "ADDRESS_NOT_VALID": ADDRESS_NOT_VALID_ERROR,
    }
# src.command.insert_email.py messages
INSERT_EMAIL_MESSAGES = {
    "INVALID_SYNTAX": "Invalid syntax. Usage: insert-email <name> <email>",
    "NO_SUCH_USER": "No such user",
    "EMAIL_ADDED": "Email added: {email} for {name}",
    "EMAIL_REPLACED": "Email replaced: {old_email} with {new_email} for {name}",
    "EMAIL_NOT_VALID": "Email is not valid",
    }
# src.command.insert_text.py messages
INSERT_TEXT_MESSAGES = {
    "INVALID_SYNTAX": "Insert text command should have the following syntax: insert-text <title> <text*>",
    "NO_TEXT": "No text",
    "NO_SUCH_NOTE": "No such note",
    "TEXT_INSERTED": "Text inserted",
    }
# src.command.remove_contact.py messages
REMOVE_CONTACT_MESSAGES = {
    "CONTACT_NOT_FOUND": "Contact {name} not found",
    "CONTACT_REMOVED": "Contact {name} removed",
    "INVALID_SYNTAX": "Remove contact command should have the following syntax: remove <name> [phone]",
    "PHONE_NOT_FOUND": "Phone {phone} not found for contact {name}",
    "PHONE_REMOVED": "Phone {phone} removed from contact {name}",
    }