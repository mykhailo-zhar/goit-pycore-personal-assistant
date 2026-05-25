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
    """
    Given a valid name and phone value
    When a Record is created and the phone is added
    Then the name and phone are stored on the record
    """
    record = Record(valid_name)
    record.add_phone(valid_phone.value)
    assert record.name.value == valid_name
    assert valid_phone.value in [phone.value for phone in record.phones]


def test_record_init_invalid_name(invalid_name):
    """
    Given an invalid name (non-string)
    When Record is constructed with that name
    Then ValueError is raised
    """
    with pytest.raises(ValueError):
        Record(invalid_name)


def test_record_add_same_phone(record, valid_phone):
    """
    Given a record that already has a phone
    When the same phone is added again
    Then ValueError is raised
    """
    with pytest.raises(ValueError):
        record.add_phone(valid_phone.value)


def test_record_add_invalid_phone(record, invalid_phone):
    """
    Given a record with a valid phone
    When an invalid phone value is added
    Then ValueError is raised
    """
    with pytest.raises(ValueError):
        record.add_phone(invalid_phone.value)


def test_record_remove_phone(record, valid_phone):
    """
    Given a record with a stored phone
    When remove_phone is called with that phone
    Then it returns True and the phone is no longer on the record
    """
    assert record.remove_phone(valid_phone.value)
    assert valid_phone not in record.phones


def test_record_remove_non_existent_phone(record, valid_phone):
    """
    Given a record after its only phone was removed
    When remove_phone is called again with the same phone
    Then it returns False
    """
    record.remove_phone(valid_phone.value)
    assert not record.remove_phone(valid_phone.value)


def test_record_find_phone(record, valid_phone):
    """
    Given a record with a stored phone
    When find_phone is called with that phone value
    Then the matching Phone object is returned
    """
    assert record.find_phone(valid_phone.value).value == valid_phone.value


def test_record_find_non_existent_phone(record, invalid_phone):
    """
    Given a record without the searched phone
    When find_phone is called with a non-existent value
    Then None is returned
    """
    assert record.find_phone(invalid_phone.value) is None


def test_record_edit_phone(record, valid_phone):
    """
    Given a record with a stored phone
    When edit_phone replaces it with a new valid phone
    Then the new phone can be found on the record
    """
    phone_value = "1234567891"
    record.edit_phone(valid_phone.value, phone_value)
    assert record.find_phone(phone_value).value == phone_value


def test_record_edit_non_existent_phone(record, valid_phone):
    """
    Given a record with no phones after removal
    When edit_phone is called for the old phone
    Then ValueError is raised
    """
    record.remove_phone(valid_phone.value)
    with pytest.raises(ValueError):
        record.edit_phone(valid_phone.value, "1234567891")


def test_record_edit_invalid_phone(record, valid_phone, invalid_phone):
    """
    Given a record with a valid phone
    When edit_phone is called with an invalid new phone
    Then ValueError is raised
    """
    with pytest.raises(ValueError):
        record.edit_phone(valid_phone.value, invalid_phone.value)


def test_fresh_record_has_no_birthday(record):
    """
    Given a newly created record with only a phone
    When birthday is accessed
    Then it is None
    """
    assert record.birthday is None


def test_record_add_birthday(record):
    """
    Given a record without a birthday
    When add_birthday is called with a valid date
    Then the birthday is stored on the record
    """
    record.add_birthday("10.01.1990")
    assert record.birthday.value == "10.01.1990"


def test_record_add_invalid_birthday(record):
    """
    Given a record without a birthday
    When add_birthday is called with an invalid date
    Then ValueError is raised
    """
    with pytest.raises(ValueError):
        record.add_birthday("10.13.1990")


def test_record_add_birthday_to_existing_record(record):
    """
    Given a record that already has a birthday
    When add_birthday is called with a new valid date
    Then the birthday is replaced with the new value
    """
    record.add_birthday("10.01.1990")
    record.add_birthday("11.01.1990")
    assert record.birthday.value == "11.01.1990"
