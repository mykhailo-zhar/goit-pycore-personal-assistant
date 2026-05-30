from src.utils.decorators.input_error import input_error
from src.address_book import AddressBook

TEAM_MEMBERS = [
    {
        "name": "Mykhailo Zhar",
        "email": "mykhailo.zhar@stud.onu.edu.ua",
        },
    {
        "name": "Kostiantyn Krysenko",
        "email": "konstantinks@gmail.com",
        },
    {
        "name": "Olga Pushkar",
        "email": "gglolga@gmail.com",
        },
    {
        "name": "Mykhailo Kovalchuk",
        "email": "mykhailokovalchuck@gmail.com",
        },
    {
        "name": "Gleb Kislovskyi",
        "email": "gkislovskyi@gmail.com",
        },
    ]


@input_error
def about_command(_: AddressBook, arguments: list[str]) -> str:
    """
    Показує інформацію про команду розробників.

    Аргументи:
        None

    Повертає:
        str: Інформація про команду.
    """
    lines = ["PERSONAL ASSISTANT", "  development by team:\n"]

    for member in TEAM_MEMBERS:
        lines.append(f"  {member['name']}")
        lines.append(f"    Email: {member['email']}")
        lines.append("")

    return "\n".join(lines)
