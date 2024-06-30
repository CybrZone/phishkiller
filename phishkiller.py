import threading
import requests
import random
import string
import names
import subprocess
import json

from fake_useragent import UserAgent

from email_gen import generate_random_email


def name_gen():#Generates a random name for the email
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":#JohnDoe
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":#JohnD
        return first_name + last_name[0]
    return first_name[0] + last_name#JDoe

def generate_random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def send_posts(url,email_domains,word_list):
    while True:
        email = generate_random_email(email_domains,word_list)
        password = generate_random_password()
        data = {"a": email, "az": password}
        ua = UserAgent()
        user_agent = ua.random
        headers = {'User-Agent': user_agent}
        response = requests.post(url, data=data, headers=headers,)
        print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}, headers: {user_agent}")

def main():
    url = input("Enter the URL of the target you want to flood: ")
    with open("domains.json") as f:
        email_domains = json.load(f)
    with open("words.json") as f:
        word_list = json.load(f)  # word list from https://www.mit.edu/~ecprice/wordlist.10000
    threads = [threading.Thread(target=send_posts, args=(url,email_domains,word_list), daemon=True) for _ in range(25)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
