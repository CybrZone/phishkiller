import random
import string

def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(12, 20)
    return "".join(random.choice(characters) for _ in range(length))
