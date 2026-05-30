import random
import string


def random_text(k=30):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))
