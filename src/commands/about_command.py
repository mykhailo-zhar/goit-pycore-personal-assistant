from src.utils.decorators.input_error import input_error
from src.address_book import AddressBook

TEAM_MEMBERS = [
    {
        "name": "Mykhailo Zhar",
        "github": "https://github.com/username",
        "linkedin": "https://linkedin.com/in/username",
        "email": "mykhailo.zhar@stud.onu.edu.ua",
        },
    {
        "name": "Kostiantyn Krysenko",
        "github": "https://github.com/barkode",
        "linkedin": "https://www.linkedin.com/in/kostiantyn-krysenko/",
        "email": "konstantinks@gmail.com",
        },
    {
        "name": "Olga Pushkar",
        "github": "https://github.com/username",
        "linkedin": "https://linkedin.com/in/username",
        "email": "gglolga@gmail.com",
        },
    {
        "name": "Mykhailo Kovalchuk",
        "github": "https://github.com/username",
        "linkedin": "https://linkedin.com/in/username",
        "email": "mykhailokovalchuck@gmail.com",
        },
    {
        "name": "Gleb Kislovskyi",
        "github": "https://github.com/username",
        "linkedin": "https://linkedin.com/in/username",
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
        lines.append(f"    GitHub:   {member['github']}")
        lines.append(f"    LinkedIn: {member['linkedin']}")
        lines.append(f"    Email: {member['email']}")
        lines.append("")

    return "\n".join(lines)
