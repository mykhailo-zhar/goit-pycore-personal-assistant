from rich.markup import escape

from src.address_book import AddressBook
from src.decorators.input_error import input_error

_CMD = "[bold green]{name}[/bold green]"
_PARAM = "[cyan]{name}[/cyan]"
_DESC = "[dim]{text}[/dim]"
_SECTION = "[bold underline]{title}[/bold underline]"


def _opt(name: str) -> str:
    return f"[blue]{escape(f'[{name}]')}[/blue]"


def _cmd(name: str, *syntax: str, desc: str) -> str:
    parts = " ".join(syntax)
    line = f"    {_CMD.format(name=name)}"
    if parts:
        line += f" {parts}"
    return f"{line:<58} {_DESC.format(text=desc)}"


@input_error
def help(_: AddressBook, arguments: list[str]) -> str:
    """
    Показує довідку по командам.

    Аргументи:
        None

    Повертає:
        str: Довідка по командам.
    """
    p = _PARAM.format
    usage_placeholders = f"  {escape('[command]')} {escape('[arguments]')}"
    return f"""[bold]USAGE:[/bold]
{usage_placeholders}

[bold magenta]AVAILABLE COMMANDS:[/bold magenta]

  {_SECTION.format(title="General")}
{_cmd("hello", desc="Greet the user.")}
{_cmd("help", desc="Show this help message.")}
{_cmd("about", desc="Show information about the development team.")}
{_cmd("all", desc="Show all contacts.")}
{_cmd("exit, close", desc="Exit the program.")}

  {_SECTION.format(title="Contacts")}
{_cmd("add", p(name="<name>"), p(name="<phone>"), desc="Add a contact or a phone to an existing contact.")}
{_cmd("truncate", p(name="<name>"), p(name="<phone>"), desc="Replace all phones with a single new phone.")}
{_cmd("change-phone", p(name="<name>"), p(name="<old>"), p(name="<new>"), desc="Change one phone number for a contact.")}
{_cmd("remove", p(name="<name>"), _opt("phone"), desc="Remove a contact, or one phone from a contact.")}
{_cmd("contact", p(name="<name>"), desc="Show full contact details by name.")}
{_cmd("contact-address", p(name="<address*>"), desc="Find contacts whose address contains the given text.")}
{_cmd("contact-email", p(name="<email>"), desc="Find a contact by exact email.")}
{_cmd("find-address", p(name="<address*>"), desc="List contacts whose address contains the given text.")}
{_cmd("insert-address", p(name="<name>"), p(name="<address*>"), desc="Add or replace a contact's address.")}
{_cmd("insert-email", p(name="<name>"), p(name="<email>"), desc="Add or replace a contact's email.")}

  {_SECTION.format(title="Birthdays")}
{_cmd("insert-birthday", p(name="<name>"), p(name="<DD.MM.YYYY>"), desc="Add or replace a contact's birthday.")}
{_cmd("show-birthday", p(name="<name>"), desc="Show a contact's birthday.")}
{_cmd("birthdays", p(name="<days>"), desc="Show upcoming birthdays within the next N days.")}

  {_SECTION.format(title="Notes")}
{_cmd("add-note", p(name="<title>"), desc="Create an empty note with the given title.")}
{_cmd("remove-note", p(name="<title>"), desc="Remove a note by title.")}
{_cmd("insert-text", p(name="<title>"), p(name="<text*>"), desc="Set or replace a note's text.")}
{_cmd("change-title", p(name="<old_title>"), p(name="<new_title>"), desc="Rename a note.")}
{_cmd("note", p(name="<title>"), desc="Show a note (title, text, and tags).")}

  {_SECTION.format(title="Tags")}
{_cmd("add-tag", p(name="<title>"), p(name="<tag>"), desc="Add a tag to a note.")}
{_cmd("remove-tag", p(name="<title>"), p(name="<tag>"), desc="Remove a tag from a note.")}
{_cmd("tag", p(name="<tag>"), p(name="<ascending|descending>"), desc="List notes with the tag, sorted by title.")}

[bold]EXAMPLES:[/bold]
  [dim]$[/dim] {_CMD.format(name="add")} John {p(name="1234567890")}
  [dim]$[/dim] {_CMD.format(name="insert-birthday")} Jane {p(name="25.12.1990")}
  [dim]$[/dim] {_CMD.format(name="add-note")} ideas
  [dim]$[/dim] {_CMD.format(name="insert-text")} ideas Buy milk and bread
  [dim]$[/dim] {_CMD.format(name="tag")} urgent {p(name="ascending")}"""
