from src.scripts.contacts_bot import COMMAND_MESSAGES, add_contact, show_all


def test_show_all_empty_and_sorted_lines(empty_address_book, valid_phone_generator):
    """Перевіряє вивід усіх контактів до і після наповнення.

    Дано:
        Порожня книга, потім додаються Amy, JohnDoe і Zed.
    Коли:
        ``show_all`` викликається до і після додавання контактів.
    Тоді:
        Спочатку повідомлення про порожню книгу, потім заголовок і контакти за іменем.

    Args:
        empty_address_book: Адресна книга.
        valid_phone_generator: Генератор валідних номерів.
    """
    assert show_all(empty_address_book) == COMMAND_MESSAGES["NO_USERS"]
    add_contact(empty_address_book, ["JohnDoe", valid_phone_generator()])
    add_contact(empty_address_book, ["Zed", valid_phone_generator()])
    add_contact(
        empty_address_book, ["Amy", valid_phone_generator(), valid_phone_generator()]
    )
    out = show_all(empty_address_book)
    assert f"Stored users ({len(empty_address_book.data)}):" in out
    assert all(
        f"{name}: {'; '.join(phone.value for phone in record.phones)}" in out
        for name, record in sorted(empty_address_book.data.items())
    )
