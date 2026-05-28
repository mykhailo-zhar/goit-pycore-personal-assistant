import re
from src.fields.field import Field


class Tag(Field):
  """Клас для зберігання тегів контакту.

  Аргументи:
        Field: Базовий клас для всіх полів.
  """    
  TAG_PATTERN = re.compile(r"^[a-z0-9]{1,30}$")

  def validate(self):
    """Перевіряє теги.

    Повертає:
        bool: True, якщо теги валідні, інакше False.
    """
    return re.match(self.TAG_PATTERN, self.value) is not None