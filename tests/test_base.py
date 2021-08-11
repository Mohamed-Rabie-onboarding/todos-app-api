"""
    load env variable as its required for some methods to work
"""
import random
import string
from app.serve import load_env_if_dev

load_env_if_dev()


class TestHelpers:

    @staticmethod
    def random_string(n=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(n))
