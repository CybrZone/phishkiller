#!/usr/bin/python3

import threading
import requests
import random
import logging
import time
import typer
from fake_useragent import UserAgent
from Assets.utils import *
from Assets.header import header
from Assets.constants import *
from Assets.utils import *
from colorama import Fore, Back, Style


# Set up logging to have some colors
logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

def send_posts(url: str, fields: dict):
	while True:
		try:
			email = generate_random_email()
			password = generate_random_password()
			username = name_gen() 

			data = {}

			if ("username" in fields.keys()):
				data[fields["username"]] = username
			if ("email" in fields.keys()):
				data[fields["email"]] = email
			if ("password" in fields.keys()):
				data[fields["password"]] = password


			ua = UserAgent()
			user_agent = ua.random
			headers = {"User-Agent": user_agent}

			response = requests.post(url, json=data, headers=headers)
			# Show fields only if they are present

			# print(f"{Back.YELLOW}{data}{Back.RESET}")

			if ("username" in fields.keys()):
				logger.info(f'{Fore.MAGENTA}Username{Fore.RESET} ({Fore.LIGHTBLACK_EX}{fields["username"]}{Fore.RESET}): {username}')
			if ("email" in fields.keys()):
				logger.info(f'{Fore.MAGENTA}Email{Fore.RESET} ({Fore.LIGHTBLACK_EX}{fields["email"]}{Fore.RESET}): {email}')
			if ("password" in fields.keys()):
				logger.info(f'{Fore.MAGENTA}Password{Fore.RESET} ({Fore.LIGHTBLACK_EX}{fields["password"]}{Fore.RESET}): {password}')

			logger.info(f"{Fore.MAGENTA}userAgent{Fore.RESET}: {user_agent}")
			logger.info(f"{Fore.MAGENTA}Status Code{Fore.RESET}: {response.status_code}")
	
			if response.status_code != 200:
				st = random.uniform(1, 5)
				logger.warning(f"{Back.CYAN}Status code {Style.BRIGHT}{response.status_code}{Style.RESET} sleeping for {Style.BRIGHT}{st}{Style.RESET}")
				time.sleep(st)  # Random delay between 1 and 5 seconds

		except requests.RequestException as e:
			logger.critical(f"Request failed: {e}")
			time.sleep(5)  # Wait for 5 seconds before retrying
			
		except Exception as e:
			logger.critical(f"An unexpected error occurred: {e}")
			time.sleep(5)  # Wait for 5 seconds before retrying


# TODO:
# 		- Add more fields like birtdays, phone numbers, first name, last name, ...
# 		- Add a cli utility with typer (it's already implemented just need to add flags, try: python3 phishkiller.py --help)


def main():
	header()
	url = input(f"[{Fore.GREEN}+{Fore.RESET}] Enter the URL of the target you want to flood: ")
	if (url):
		print(f"\t{Fore.GREEN}--> {Fore.RESET} url: {url}\n")
	selected_fields = {}

	for f in fields:
		field = input(f"[{Fore.GREEN}+{Fore.RESET}] Enter {Fore.CYAN}{f}{Fore.RESET} field {Fore.LIGHTBLACK_EX}(blank if not used){Fore.RESET}: ")
		if (field):
			selected_fields[f] = field
	if (len(selected_fields) == 0):
		print(EMPTY_FIELDS_ERROR)
		exit(1)
	print(f"\n[{Fore.GREEN}+{Fore.RESET}] The program will start soon...\n")
	time.sleep(3)
	try:
	    threads = [
	        threading.Thread(target=send_posts, args=(url,selected_fields,), daemon=True)
	        for _ in range(25)
	    ]

	    for t in threads:
	        t.start()

	    for t in threads:
	        t.join()
	except Exception as e:
	    print(f"Error in main: {e}")


if __name__ == "__main__":
	typer.run(main)

