class MessageManager:

    def __init__(self):
        # src.scripts.contacts_bot.py messages
        self.command_messages = {
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
        self.add_note_messages = {
            "INVALID_SYNTAX": "Add note command should have the following syntax: add-note <title>",
            "NOTE_ALREADY_PRESENT": "Note is already present.",
            "NOTE_ADDED": "Note added: {title}",
            }

        # src.commands.add_tag.py messages
        self.add_tag_messages = {
            "INVALID_SYNTAX": "Add tag command should have the following syntax: add-tag <title> <tag>",
            "NO_SUCH_NOTE": "There is no such note",
            "TAG_ALREADY_EXISTS": "There is already such tag",
            "TAG_ADDED": "Tag added",
            }

        # src.command.change_title.py messages
        self.change_title_messages = {
            "INVALID_SYNTAX": "Change title command should have the following syntax: change-title <old_title> <new_title>",
            "NO_SUCH_NOTE": "No such note",
            "NOTE_ALREADY_EXISTS": "Note already exists",
            "TITLE_CHANGED": "Title was changed",
            }
        # src.command.find_by_tag.py messages
        self.find_by_tag_messages = {
            "INVALID_SYNTAX": "Tag command should have the following syntax: tag <tag> <order>",
            "INVALID_ORDER": "There are only ascending and descending order.",
            "NO_NOTES": "There are no notes,",
            }
        # src.command.find_by_tag.py messages
        self.insert_address_messages = {
            "INVALID_SYNTAX": "Insert address command should have the following syntax: insert-address <name> <address>",
            "ADDRESS_ADDED": "Address added.",
            "ADDRESS_REPLACED": "Replacing {old_address} with {new_address} for {name}",
            "NO_SUCH_CONTACT": "No such contact.",
            "ADDRESS_NOT_VALID": self.record_messages.ADDRESS_NOT_VALID_ERROR,
            }
        # src.command.insert_email.py messages
        self.insert_email_messages = {
            "INVALID_SYNTAX": "Invalid syntax. Usage: insert-email <name> <email>",
            "NO_SUCH_USER": "No such user",
            "EMAIL_ADDED": "Email added: {email} for {name}",
            "EMAIL_REPLACED": "Email replaced: {old_email} with {new_email} for {name}",
            "EMAIL_NOT_VALID": "Email is not valid",
            }
        # src.command.insert_text.py messages
        self.insert_text_messages = {
            "INVALID_SYNTAX": "Insert text command should have the following syntax: insert-text <title> <text*>",
            "NO_TEXT": "No text",
            "NO_SUCH_NOTE": "No such note",
            "TEXT_INSERTED": "Text inserted",
            }
        # src.command.remove_contact.py messages
        self.remove_contact_messages = {
            "CONTACT_NOT_FOUND": "Contact {name} not found",
            "CONTACT_REMOVED": "Contact {name} removed",
            "INVALID_SYNTAX": "Remove contact command should have the following syntax: remove <name> [phone]",
            "PHONE_NOT_FOUND": "Phone {phone} not found for contact {name}",
            "PHONE_REMOVED": "Phone {phone} removed from contact {name}",
            }
        # src.command.remove_tag.py messages
        self.remove_tag_messages = {
            "INVALID_SYNTAX": "Remove tag command should have the following syntax: remove-tag <title> <tag>",
            "NO_SUCH_NOTE": "There is no such note",
            "NO_TAG_ON_NOTE": "There is no tag on the note",
            "TAG_REMOVED": "Tag removed",
            }
        # src.command.show_all.py messages
        self.show_all_messages = {
            "INVALID_SYNTAX": "Invalid command.",
            "NO_USERS": "There are no users.",
            }
        # src.command.show_note.py messages
        self.show_note_messages = {
            "INVALID_SYNTAX": "Note command should have the following syntax: note <title>",
            "NO_SUCH_NOTE": "No such note",
            "TITLE_LABEL": "Note title: ",
            "TEXT_LABEL": "text: ",
            "TAGS_LABEL": "tags: ",
            }
        # src.record.py messages
        self.record_messages = {
            "PHONE_NOT_FOUND_ERROR": "Phone not found",
            "PHONE_NOT_VALID_ERROR": "Phone is not valid",
            "PHONE_ALREADY_EXISTS_ERROR": "Phone already exists",
            "NAME_NOT_VALID_ERROR": "Name is not valid, must be a non-empty alphanumeric string",
            "BIRTHDAY_NOT_VALID_ERROR": (
                "Birthday {birthday} is not valid, must be in the format DD.MM.YYYY"
            ),
            "EMAIL_NOT_VALID_ERROR": "Email is not valid",
            "ADDRESS_NOT_VALID_ERROR": "Address is not valid",
            }


mess = MessageManager()

COMMAND_MESSAGES = mess.command_messages
ADD_NOTE_MESSAGES = mess.add_note_messages
ADD_TAG_MESSAGES = mess.add_tag_messages
CHANGE_TITLE_MESSAGES = mess.change_title_messages
FIND_BY_TAG_MESSAGES = mess.find_by_tag_messages
INSERT_ADDRESS_MESSAGES = mess.insert_address_messages
INSERT_EMAIL_MESSAGES = mess.insert_email_messages
INSERT_TEXT_MESSAGES = mess.insert_text_messages
REMOVE_CONTACT_MESSAGES = mess.remove_contact_messages
REMOVE_TAG_MESSAGES = mess.remove_tag_messages
SHOW_ALL_MESSAGES = mess.show_all_messages
SHOW_NOTE_MESSAGES = mess.show_note_messages
RECORD_MESSAGES = mess.record_messages
