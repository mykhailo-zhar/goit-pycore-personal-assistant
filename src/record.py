from src.fields.address import Address
from src.fields.birthday import Birthday
from src.fields.email import Email
from src.fields.name import Name
from src.fields.phone import Phone

PHONE_NOT_FOUND_ERROR = "Phone not found"
PHONE_NOT_VALID_ERROR = "Phone is not valid"
PHONE_ALREADY_EXISTS_ERROR = "Phone already exists"
NAME_NOT_VALID_ERROR = "Name is not valid, must be a non-empty alphanumeric string"
BIRTHDAY_NOT_VALID_ERROR = (
    "Birthday {birthday} is not valid, must be in the format DD.MM.YYYY"
)
EMAIL_NOT_VALID_ERROR = "Email is not valid"
ADDRESS_NOT_VALID_ERROR = "Address is not valid"


class Record:
    def __init__(self, name: str):
        """
        Ініціалізує запис ім'ям контакту.

        Аргументи:
            name (str): Ім'я контакту.

        Винятки:
            ValueError: Якщо ім'я невалідне.
        """
        self.name = name
        self._phones = []
        self._birthday = None
        self._email = None
        self._address = None

    # region Properties

    @property
    def name(self) -> Name:
        """
        Повертає ім'я запису.

        Повертає:
            Name: Ім'я контакту.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Встановлює ім'я запису.

        Аргументи:
            name: Ім'я для встановлення.

        Винятки:
            ValueError: Якщо ім'я невалідне.
        """
        name_obj = Name(name)
        if not name_obj.validate():
            raise ValueError(NAME_NOT_VALID_ERROR)
        self._name = name_obj

    @property
    def birthday(self) -> Birthday | None:
        """
        Повертає день народження запису.

        Повертає:
            Birthday | None: День народження контакту.
        """
        return self._birthday

    @birthday.setter
    def birthday(self, birthday):
        """
        Встановлює день народження запису.

        Аргументи:
            birthday: День народження для встановлення.

        Винятки:
            ValueError: Якщо день народження невалідний.
        """
        birthday_obj = Birthday(birthday)
        if not birthday_obj.validate():
            raise ValueError(BIRTHDAY_NOT_VALID_ERROR.format(birthday=birthday))
        self._birthday = birthday_obj

    @property
    def phones(self) -> list[Phone]:
        """
        Повертає список телефонів запису.

        Повертає:
            list[Phone]: Список телефонів запису.
        """
        return self._phones

    @property
    def address(self) -> Address | None:
        """
        Повертає адресу запису.

        Повертає:
            Address | None: Адреса запису.
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        Встановлює адресу запису.

        Аргументи:
            address: Адреса для встановлення.

        Винятки:
            ValueError: Якщо адреса невалідна.
        """
        address_obj = Address(address)
        if not address_obj.validate():
            raise ValueError(ADDRESS_NOT_VALID_ERROR)
        self._address = address_obj

    @property
    def email(self) -> Email | None:
        """
        Повертає email запису.

        Повертає:
            Email | None: Email контакту.
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Встановлює email запису.

        Аргументи:
            email (str): Email.

        Винятки:
            ValueError: Якщо email невалідний.
        """
        email_obj = Email(email)
        if not email_obj.validate():
            raise ValueError(EMAIL_NOT_VALID_ERROR)
        self._email = email_obj

    # endregion

    # region Methods

    def add_birthday(self, birthday: str):
        """
        Додає день народження до запису.

        Аргументи:
            birthday (str): День народження у форматі DD.MM.YYYY.

        Винятки:
            ValueError: Якщо дата невалідна.
        """
        self.birthday = birthday

    def add_phone(self, phone: str):
        """
        Додає телефон до запису.

        Аргументи:
            phone (str): Номер телефону.

        Винятки:
            ValueError: Якщо номер невалідний або вже існує.
        """
        phone_obj = Phone(phone)
        if not phone_obj.validate():
            raise ValueError(PHONE_NOT_VALID_ERROR)

        if self.find_phone(phone) is not None:
            raise ValueError(PHONE_ALREADY_EXISTS_ERROR)

        self.phones.append(phone_obj)

    def remove_phone(self, phone: str) -> bool:
        """
        Видаляє телефон з запису.

        Аргументи:
            phone (str): Номер для видалення.

        Повертає:
            bool: True, якщо телефон видалено, інакше False.
        """
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove is None:
            return False
        self.phones.remove(phone_to_remove)
        return True

    def find_phone(self, phone: str) -> Phone | None:
        """
        Шукає телефон у записі.

        Аргументи:
            phone (str): Номер для пошуку.

        Повертає:
            Phone | None: Об'єкт телефону, якщо знайдено, інакше None.
        """
        return next((x for x in self.phones if x.value == phone), None)

    def edit_phone(self, old_phone, new_phone):
        """
        Замінює телефон у записі.

        Аргументи:
            old_phone: Старий номер.
            new_phone: Новий номер.

        Винятки:
            ValueError: Якщо старий номер не знайдено або новий невалідний.
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
        """
        Повертає рядкове подання запису.

        Повертає:
            str: Рядкове подання запису для виведення.
        """
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {';'.join(p.value for p in self.phones) or 'None'}, "
            f"email: {self.email.value if self.email else 'None'}, "
            f"address: {self.address.value if self.address else 'None'}"
        )
