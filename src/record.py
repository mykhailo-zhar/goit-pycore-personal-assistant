from src.fields.birthday import Birthday
from src.fields.name import Name
from src.fields.phone import Phone

PHONE_NOT_FOUND_ERROR = "Phone not found"
PHONE_NOT_VALID_ERROR = "Phone is not valid"
PHONE_ALREADY_EXISTS_ERROR = "Phone already exists"
NAME_NOT_VALID_ERROR = "Name is not valid, must be a non-empty alphanumeric string"
BIRTHDAY_NOT_VALID_ERROR = (
    "Birthday {birthday} is not valid, must be in the format DD.MM.YYYY"
)


class Record:
    def __init__(self, name: str):
        """
        Initialize the record with a name.

        Args:
            name (str): The name of the record.

        Raises:
            ValueError: If the name is not valid.
        """
        self.name = name
        self._phones = []
        self._birthday = None

    # region Properties

    @property
    def name(self) -> Name:
        """
        Get the name of the record.

        Returns:
            Name: The name of the record.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of the record.

        Args:
            name: The name to set.

        Raises:
            ValueError: If the name is not valid.
        """
        name_obj = Name(name)
        if not name_obj.validate():
            raise ValueError(NAME_NOT_VALID_ERROR)
        self._name = name_obj

    @property
    def birthday(self) -> Birthday | None:
        """
        Get the birthday of the record.

        Returns:
            Birthday | None: The birthday of the record.
        """
        return self._birthday

    @birthday.setter
    def birthday(self, birthday):
        """
        Set the birthday of the record.
        """
        birthday_obj = Birthday(birthday)
        if not birthday_obj.validate():
            raise ValueError(BIRTHDAY_NOT_VALID_ERROR.format(birthday=birthday))
        self._birthday = birthday_obj

    @property
    def phones(self) -> list[Phone]:
        """
        Get the phones of the record.
        """
        return self._phones

    # endregion

    # region Methods

    def add_birthday(self, birthday: str):
        """
        Add a birthday to the record.

        Args:
            birthday (str): The birthday to add.

        Raises:
            ValueError: If the birthday is not valid.
        """
        self.birthday = birthday

    def add_phone(self, phone: str):
        """
        Add a phone to the record.

        Args:
            phone (str): The phone number to add.

        Raises:
            ValueError: If the phone number is not valid.
        """
        phone_obj = Phone(phone)
        if not phone_obj.validate():
            raise ValueError(PHONE_NOT_VALID_ERROR)

        if self.find_phone(phone) is not None:
            raise ValueError(PHONE_ALREADY_EXISTS_ERROR)

        self.phones.append(phone_obj)

    def remove_phone(self, phone: str) -> bool:
        """
        Remove a phone from the record.

        Args:
            phone (str): The phone number to remove.

        Returns:
            bool: True if the phone number was removed, False otherwise.
        """
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove is None:
            return False
        self.phones.remove(phone_to_remove)
        return True

    def find_phone(self, phone: str) -> Phone | None:
        """
        Find a phone in the record.

        Args:
            phone (str): The phone number to find.

        Returns:
            Phone | None: The phone object if found, None otherwise.
        """
        return next((x for x in self.phones if x.value == phone), None)

    def edit_phone(self, old_phone, new_phone):
        """
        Edit a phone in the record.

        Args:
            old_phone (_type_): The old phone number to edit.
            new_phone (_type_): The new phone number to insert.

        Raises:
            ValueError: If the old phone number is not found.
            ValueError: If the new phone number is not valid.
        """
        phone_index = next(
            (i for i, x in enumerate(self.phones) if x.value == old_phone), None
        )
        if phone_index is None:
            raise ValueError(PHONE_NOT_FOUND_ERROR)

        new_phone_obj = Phone(new_phone)
        if not new_phone_obj.validate():
            raise ValueError(PHONE_NOT_VALID_ERROR)

        self.phones[phone_index] = new_phone_obj

    # endregion

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
