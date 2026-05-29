from src.fields.tag import Tag
from src.fields.text import Text
from src.fields.title import Title

NOTE_ERRORS = {
    "TITLE_NOT_VALID": "Title is not valid",
    "TEXT_NOT_VALID": "Text is not valid",
    "TAG_NOT_VALID": "Tag is not valid",
    "TAG_ALREADY_EXISTS": "Tag already exists",
}


SHOW_NOTE_MESSAGES = {
    "TITLE_LABEL": "Note title: ",
    "TEXT_LABEL": "text: ",
    "TAGS_LABEL": "tags: ",
}


class Note:
    def __init__(self, title: str):
        """
        Ініціалізує нотатку заголовком.

        Аргументи:
            title (str): Заголовок нотатки.

        Винятки:
            ValueError: Якщо заголовок невалідний.
        """
        self._tags: list[Tag] = []
        self.title = title

    @property
    def title(self) -> Title:
        """
        Повертає заголовок нотатки.

        Повертає:
            Title: Заголовок нотатки.
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """
        Встановлює заголовок нотатки.

        Аргументи:
            title (str): Заголовок для встановлення.

        Винятки:
            ValueError: Якщо заголовок невалідний.
        """
        title_obj = Title(title)
        if not title_obj.validate():
            raise ValueError(NOTE_ERRORS["TITLE_NOT_VALID"])
        self._title = title_obj

    @property
    def text(self) -> Text:
        """
        Повертає текст нотатки.

        Повертає:
            Text: Текст нотатки.
        """
        return self._text

    @text.setter
    def text(self, text: str):
        """
        Встановлює текст нотатки.

        Аргументи:
            text (str): Текст для встановлення.

        Винятки:
            ValueError: Якщо текст невалідний.
        """
        text_obj = Text(text)
        if not text_obj.validate():
            raise ValueError(NOTE_ERRORS["TEXT_NOT_VALID"])
        self._text = text_obj

    def edit_title(self, title: str):
        """
        Змінює заголовок нотатки.

        Аргументи:
            title (str): Новий заголовок.

        Винятки:
            ValueError: Якщо заголовок невалідний.
        """
        self.title = title

    def add_tag(self, tag: str):
        """
        Додає тег до нотатки.

        Аргументи:
            tag (str): Тег для додавання.

        Винятки:
            ValueError: Якщо тег невалідний або вже існує.
        """
        tag_obj = Tag(tag)
        if not tag_obj.validate():
            raise ValueError(NOTE_ERRORS["TAG_NOT_VALID"])

        if self.find_tag(tag) is not None:
            raise ValueError(NOTE_ERRORS["TAG_ALREADY_EXISTS"])

        self._tags.append(tag_obj)

    def remove_tag(self, tag: str) -> bool:
        """
        Видаляє тег з нотатки.

        Аргументи:
            tag (str): Тег для видалення.

        Повертає:
            bool: True, якщо тег видалено, інакше False.
        """
        tag_to_remove = self.find_tag(tag)
        if tag_to_remove is None:
            return False
        self._tags.remove(tag_to_remove)
        return True

    def show_tags(self) -> str:
        """
        Повертає рядок із усіма тегами нотатки.

        Повертає:
            str: Теги через кому або порожній рядок.
        """
        return ",".join(tag.value for tag in self._tags)

    def find_tag(self, tag: str) -> Tag | None:
        """
        Шукає тег в нотатці.

        Аргументи:
            tag (str): Тег для пошуку.

        Повертає:
            Tag | None: Об'єкт тегу, якщо знайдено, інакше None.
        """
        return next((tag for tag in self._tags if tag.value == tag), None)

    def __str__(self) -> str:
        parts = [f"{SHOW_NOTE_MESSAGES['TITLE_LABEL']}{self.title.value}"]
        if hasattr(self, "_text"):
            parts.append(f"{SHOW_NOTE_MESSAGES['TEXT_LABEL']}{self.text.value}")
        tags = self.show_tags()
        if tags:
            parts.append(f"{SHOW_NOTE_MESSAGES['TAGS_LABEL']}{tags}")
        return ", ".join(parts)
