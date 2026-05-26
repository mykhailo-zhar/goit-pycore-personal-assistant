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
        Ініціалізує запис ім'ям контакту.

        Аргументи:
            name (str): Ім'я контакту.

        Винятки:
            ValueError: Якщо ім'я невалідне.
        """
        self.name = name
        self._phones = []
        self._birthday = None

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
        """Встановлює день народження запису."""
        birthday_obj = Birthday(birthday)
        if not birthday_obj.validate():
            raise ValueError(BIRTHDAY_NOT_VALID_ERROR.format(birthday=birthday))
        self._birthday = birthday_obj

    @property
    def phones(self) -> list[Phone]:
        """Повертає список телефонів запису."""
        return self._phones

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

    def edit_phone(self, old_phone, new_phone) -> None:
        """
        Замінює телефон у записі.

        Аргументи:
            old_phone: Старий номер.
            new_phone: Новий номер.

        Винятки:
            ValueError: Якщо старий номер не знайдено або новий невалідний.
        """
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError(PHONE_NOT_FOUND_ERROR)

        new_phone_obj = Phone(new_phone)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj

    # endregion

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
