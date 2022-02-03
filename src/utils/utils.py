import string
import random


def random_string(length):
    return ''.join(random.sample(string.ascii_lowercase + string.digits, length))
