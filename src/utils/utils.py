import string
import random
import uuid


def random_string(length: int) -> str:
    return str(uuid.uuid4())[:length]
