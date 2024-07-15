import threading
import requests
import time
import random
import logging
from fake_useragent import UserAgent
from src.generators.emailGenerator import generate_random_email
from src.generators.passwordGenerator import generate_random_password
from src.ui.ui import console  # Import console for pretty printing

hit = [0]

def send_posts(url, posts_per_thread, hit_lock):
    for _ in range(posts_per_thread):
        try:
            email = generate_random_email()
            password = generate_random_password()
            data = {"user": email, "pass": password}
            ua = UserAgent()
            user_agent = ua.random
            headers = {"User-Agent": user_agent}

            response = requests.post(url, data=data, headers=headers)
            logging.info(
                f"Email: {email}, Password: {password}, Status Code: {response.status_code}, User-Agent: {user_agent}"
            )

            if response.status_code == 200:
                with hit_lock:
                    hit[0] += 1
                # Pretty print the email and password
                console.print(f"[bold]Email:[/bold][green] {email}[/green]  [bold]Password:[/bold][blue] {password}[/blue]")
            else:
                logging.error(f"Error: Received status code {response.status_code}")
                time.sleep(random.uniform(1, 5))

        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            time.sleep(5)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            time.sleep(5)
