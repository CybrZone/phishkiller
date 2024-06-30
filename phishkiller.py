# cSpell:ignore aiohttp UserAgent levelname protonmail KHTML


import asyncio
import aiohttp
import random
import string
import names
import logging
from fake_useragent import UserAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def name_gen():
    """Generates a random name for the email."""
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":
        return first_name + last_name[0]
    return first_name[0] + last_name

def generate_random_email():
    """Generates a random email using common domains."""
    name = name_gen()
    NumberOrNo = random.choice(["Number", "No"])
    domain = random.choice(["@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"])
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain

def generate_random_password():
    """Generates a random password with letters and digits."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

async def send_post(session, url):
    """Sends a POST request with random email and password to the target URL."""
    email = generate_random_email()
    password = generate_random_password()
    data = {"a": email, "az": password}
    try:
        ua = UserAgent()
        user_agent = ua.random
    except Exception as e:
        logging.error(f"UserAgent generation failed: {e}")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    
    headers = {'User-Agent': user_agent}
    
    try:
        async with session.post(url, data=data, headers=headers) as response:
            status = response.status
            logging.info(f"Email: {email}, Password: {password}, Status Code: {status}, Headers: {headers['User-Agent']}")
    except Exception as e:
        logging.error(f"Request failed: {e}")

async def main():
    """Main function to start the spamming process."""
    url = input("Enter the URL of the phishing link you want to kill: ")
    try:
        num_posts = int(input("Enter the number of POST requests to send: "))
    except ValueError:
        logging.error("Invalid input for number of posts. Exiting.")
        return
    
    async with aiohttp.ClientSession() as session:
        tasks = [send_post(session, url) for _ in range(num_posts)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")