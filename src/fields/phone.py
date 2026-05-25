import re

from ..fields.field import Field


class Phone(Field):
    """
    Stores the contact phone number.

    Args:
        Field: Base class for all fields.
    """

    def validate(self):
        """
        Validate the phone number.

        Returns:
            bool: True if the phone number is valid, False otherwise.
        """
        return re.match(r"^\d{10}$", self.value) is not None
