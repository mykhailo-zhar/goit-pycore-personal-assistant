from datetime import datetime

from src.fields.field import Field


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"
    """
    Stores the contact birthday.

    Args:
        Field: Base class for all fields.
    """

    def validate(self):
        """
        Validate the birthday.
        """

        try:
            datetime.strptime(self.value, self.DATE_FORMAT)
            return True
        except (ValueError, TypeError):
            return False

    def format(self, today=datetime.now()):
        """
        Format the birthday in the format DD.MM.YYYY (Weekday).

        Args:
            today (datetime): The today's date.

        Returns:
            str: The formatted birthday in the format DD.MM.YYYY (Weekday).
        """
        birthdate = datetime.strptime(self.value, self.DATE_FORMAT)
        birthdate = birthdate.replace(year=today.year)
        return birthdate.strftime(f"{self.DATE_FORMAT} (%A)")
