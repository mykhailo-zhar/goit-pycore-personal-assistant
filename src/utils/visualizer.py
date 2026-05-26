from colorama import Fore, Style, init
from prettytable import PrettyTable

# Ініціалізація colorama
init(autoreset=True)

# Створюємо власні змінні для пастельного жовтого кольору за вашими RGB (255, 255, 204)
PASTEL_YELLOW = "\033[38;2;255;255;153m"
RESET = Style.RESET_ALL

def display_address_book(records):
    """
    Виводить список записів у вигляді красивої таблиці з чергуванням пастельно-жовтих рядків (RGB 255 255 204).
    """
    table = PrettyTable()
    
    # Заголовки колонок (Cyan)
    table.field_names = [
        f"{Fore.CYAN}Name{RESET}",
        f"{Fore.CYAN}Birthday{RESET}",
        f"{Fore.CYAN}Address{RESET}",
        f"{Fore.CYAN}Telephone#{RESET}",
        f"{Fore.CYAN}Email{RESET}",
        f"{Fore.CYAN}Notes{RESET}"
    ]
    
    table.align = "l"

    if hasattr(records, "values"):
        records = records.values()

    records_list = list(records)

    if not records_list:
        print(f"{Fore.YELLOW}Адресна книга порожня або записів не знайдено.{RESET}")
        return

    # Використовуємо enumerate, щоб отримати індекс (i) кожного рядка
    for i, record in enumerate(records_list):
        # 1. Збираємо чисті текстові значення
        name = record.name.value if record.name else "-"
        birthday = record.birthday.value if record.birthday else "-"
        phones = ", ".join([str(p.value) for p in record.phones]) if record.phones else "-"
        
        address = record.address.value if hasattr(record, 'address') and record.address else "-"
        email = record.email.value if hasattr(record, 'email') and record.email else "-"
        
        notes = "-"
        if hasattr(record, 'notes') and record.notes:
            text = record.notes.text if hasattr(record.notes, 'text') else str(record.notes)
            tags = f" [{', '.join(record.notes.tags)}]" if hasattr(record.notes, 'tags') and record.notes.tags else ""
            notes = f"{text}{tags}"

        # 2. Перевіряємо, чи це непарний рядок (кожен другий)
        if i % 2 == 1:
            # Застосовуємо м'який пастельний RGB-колір
            name = f"{PASTEL_YELLOW}{name}{RESET}"
            birthday = f"{PASTEL_YELLOW}{birthday}{RESET}"
            address = f"{PASTEL_YELLOW}{address}{RESET}"
            phones = f"{PASTEL_YELLOW}{phones}{RESET}"
            email = f"{PASTEL_YELLOW}{email}{RESET}"
            notes = f"{PASTEL_YELLOW}{notes}{RESET}"

        # Додаємо рядок у таблицю
        table.add_row([name, birthday, address, phones, email, notes])

    print(f"\n{Fore.BLUE}{table}{RESET}\n")
