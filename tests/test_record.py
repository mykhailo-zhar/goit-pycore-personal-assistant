import pytest

from src.fields.phone import Phone
from src.record import Record


@pytest.fixture
def valid_name():
    return "John"


@pytest.fixture
def invalid_name():
    return 10


@pytest.fixture
def valid_phone():
    return Phone("1234567890")


@pytest.fixture
def invalid_phone():
    return Phone("12345678901")


@pytest.fixture
def record(valid_name, valid_phone):
    rec = Record(valid_name)
    rec.add_phone(valid_phone.value)
    return rec


def test_record_init(valid_name, valid_phone):
    """Перевіряє збереження імені та телефону при створенні запису.

    Дано:
        Валідне ім'я та номер телефону.
    Коли:
        Створюється ``Record`` і додається телефон.
    Тоді:
        Ім'я та номер зберігаються в записі.

    Args:
        valid_name: Валідне ім'я контакту.
        valid_phone: Валідний об'єкт ``Phone`` (10 цифр).
    """
    record = Record(valid_name)
    record.add_phone(valid_phone.value)
    assert record.name.value == valid_name
    assert valid_phone.value in [phone.value for phone in record.phones]


def test_record_init_invalid_name(invalid_name):
    """Перевіряє відхилення невалідного імені при створенні запису.

    Дано:
        Невалідне ім'я (не рядок).
    Коли:
        Створюється ``Record`` з цим іменем.
    Тоді:
        Виникає ``ValueError``.

    Args:
        invalid_name: Невалідне значення імені.
    """
    with pytest.raises(ValueError):
        Record(invalid_name)


def test_record_add_same_phone(record, valid_phone):
    """Перевіряє заборону дублювання телефону в записі.

    Дано:
        Запис, у якого вже є цей телефон.
    Коли:
        Той самий телефон додається знову.
    Тоді:
        Виникає ``ValueError``.

    Args:
        record: Запис із одним телефоном.
        valid_phone: Валідний об'єкт ``Phone``.
    """
    with pytest.raises(ValueError):
        record.add_phone(valid_phone.value)


def test_record_add_invalid_phone(record, invalid_phone):
    """Перевіряє відхилення невалідного номера при додаванні.

    Дано:
        Запис із валідним телефоном.
    Коли:
        Додається невалідний номер.
    Тоді:
        Виникає ``ValueError``.

    Args:
        record: Запис із валідним телефоном.
        invalid_phone: Невалідний об'єкт ``Phone``.
    """
    with pytest.raises(ValueError):
        record.add_phone(invalid_phone.value)


def test_record_remove_phone(record, valid_phone):
    """Перевіряє успішне видалення існуючого телефону.

    Дано:
        Запис із збереженим телефоном.
    Коли:
        Викликається ``remove_phone`` для цього номера.
    Тоді:
        Повертається ``True`` і телефон видаляється з запису.

    Args:
        record: Запис із телефоном.
        valid_phone: Телефон для видалення.
    """
    assert record.remove_phone(valid_phone.value)
    assert valid_phone not in record.phones


def test_record_remove_non_existent_phone(record, valid_phone):
    """Перевіряє видалення вже відсутнього телефону.

    Дано:
        Запис після видалення єдиного телефону.
    Коли:
        ``remove_phone`` викликається знову для того ж номера.
    Тоді:
        Повертається ``False``.

    Args:
        record: Запис без телефонів.
        valid_phone: Номер, який уже видалено.
    """
    record.remove_phone(valid_phone.value)
    assert not record.remove_phone(valid_phone.value)


def test_record_find_phone(record, valid_phone):
    """Перевіряє пошук існуючого телефону в записі.

    Дано:
        Запис із збереженим телефоном.
    Коли:
        Викликається ``find_phone`` для цього номера.
    Тоді:
        Повертається відповідний об'єкт ``Phone``.

    Args:
        record: Запис із телефоном.
        valid_phone: Шуканий номер.
    """
    assert record.find_phone(valid_phone.value).value == valid_phone.value


def test_record_find_non_existent_phone(record, invalid_phone):
    """Перевіряє пошук неіснуючого телефону.

    Дано:
        Запис без шуканого телефону.
    Коли:
        Викликається ``find_phone`` для неіснуючого номера.
    Тоді:
        Повертається ``None``.

    Args:
        record: Запис без цього номера.
        invalid_phone: Номер, якого немає в записі.
    """
    assert record.find_phone(invalid_phone.value) is None


def test_record_edit_phone(record, valid_phone):
    """Перевіряє заміну телефону на новий валідний номер.

    Дано:
        Запис із збереженим телефоном.
    Коли:
        ``edit_phone`` замінює його на новий валідний номер.
    Тоді:
        Новий телефон знаходиться в записі.

    Args:
        record: Запис із телефоном.
        valid_phone: Старий номер для заміни.
    """
    phone_value = "1234567891"
    record.edit_phone(valid_phone.value, phone_value)
    assert record.find_phone(phone_value).value == phone_value


def test_record_edit_non_existent_phone(record, valid_phone):
    """Перевіряє редагування відсутнього телефону.

    Дано:
        Запис без телефонів після видалення.
    Коли:
        Викликається ``edit_phone`` для старого номера.
    Тоді:
        Виникає ``ValueError``.

    Args:
        record: Порожній за телефонами запис.
        valid_phone: Номер, якого вже немає.
    """
    record.remove_phone(valid_phone.value)
    with pytest.raises(ValueError):
        record.edit_phone(valid_phone.value, "1234567891")


def test_record_edit_invalid_phone(record, valid_phone, invalid_phone):
    """Перевіряє відхилення невалідного нового номера при редагуванні.

    Дано:
        Запис із валідним телефоном.
    Коли:
        ``edit_phone`` викликається з невалідним новим номером.
    Тоді:
        Виникає ``ValueError``.

    Args:
        record: Запис із валідним телефоном.
        valid_phone: Поточний номер.
        invalid_phone: Невалідний новий номер.
    """
    with pytest.raises(ValueError):
        record.edit_phone(valid_phone.value, invalid_phone.value)


def test_fresh_record_has_no_birthday(record):
    """Перевіряє відсутність дня народження у новому записі.

    Дано:
        Щойно створений запис лише з телефоном.
    Коли:
        Зчитується ``birthday``.
    Тоді:
        Значення ``None``.

    Args:
        record: Новий запис без дня народження.
    """
    assert record.birthday is None


def test_record_add_birthday(record):
    """Перевіряє додавання валідного дня народження.

    Дано:
        Запис без дня народження.
    Коли:
        Викликається ``add_birthday`` з валідною датою.
    Тоді:
        День народження зберігається в записі.

    Args:
        record: Запис без дня народження.
    """
    record.add_birthday("10.01.1990")
    assert record.birthday.value == "10.01.1990"


def test_record_add_invalid_birthday(record):
    """Перевіряє відхилення невалідної дати народження.

    Дано:
        Запис без дня народження.
    Коли:
        Викликається ``add_birthday`` з невалідною датою.
    Тоді:
        Виникає ``ValueError``.

    Args:
        record: Запис без дня народження.
    """
    with pytest.raises(ValueError):
        record.add_birthday("10.13.1990")


def test_record_add_birthday_to_existing_record(record):
    """Перевіряє заміну існуючого дня народження.

    Дано:
        Запис, у якого вже є день народження.
    Коли:
        Викликається ``add_birthday`` з новою валідною датою.
    Тоді:
        День народження замінюється новим значенням.

    Args:
        record: Запис із наявним днем народження.
    """
    record.add_birthday("10.01.1990")
    record.add_birthday("11.01.1990")
    assert record.birthday.value == "11.01.1990"
