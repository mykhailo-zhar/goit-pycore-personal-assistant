import builtins

from src.scripts.contacts_bot import COMMAND_MESSAGES, main
from src.utils.address_book_serializer import AddressBookSerializer


def test_main_prints_replies_and_goodbye(
    monkeypatch, capsys, valid_phone_generator, tmp_path
):
    file_path = str(tmp_path / "address_book.pkl")
    serializer = AddressBookSerializer(file_path)
    phone1 = valid_phone_generator()
    phone2 = valid_phone_generator()
    lines = iter(
        [
            "hello",
            f"add Pat {phone1}",
            f"add Pat {phone2}",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    monkeypatch.setattr(
        "src.scripts.contacts_bot.SERIALIZER_PATH",
        file_path,
    )
    main()

    out = capsys.readouterr().out
    assert COMMAND_MESSAGES["HELLO"] in out
    assert COMMAND_MESSAGES["CONTACT_ADDED"] in out
    assert COMMAND_MESSAGES["GOOD_BYE"] in out
    deserialized_address_book = serializer.deserialize()
    assert len(deserialized_address_book.data) == 1
    assert deserialized_address_book.data["Pat"].phones[0].value == phone1
    assert deserialized_address_book.data["Pat"].phones[1].value == phone2
