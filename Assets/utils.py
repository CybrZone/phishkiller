import random
import names
import string
import logging
from colorama import Fore, Style
from Assets.emailHosts import weighted_email_domains

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


def generate_random_email():
	# Generate email with combination of name and domain
	name = name_gen()
	use_number = random.choice([True, False])  # Renamed for clarity
	
	# Calculate cumulative weights
	cumulative_weights = []
	total_weight = 0
	for domain, weight in weighted_email_domains:
		total_weight += weight
		cumulative_weights.append((domain, total_weight))
	
	# Select domain based on cumulative weights
	random_number = random.randint(1, total_weight)
	for domain, cumulative_weight in cumulative_weights:
		if random_number <= cumulative_weight:
			selected_domain = domain
			break
	
	# Generate email with or without a number
	if use_number:
		return f"{name}{random.randint(1, 100)}{selected_domain}"
	else:
		return f"{name}{selected_domain}"


def generate_random_password():  # Generate password using uppercase, lowercase, numbers and special characters
	characters = string.ascii_letters + string.digits + string.punctuation
	length = random.randint(12, 20)  # Random length between 12 and 20
	return "".join(random.choice(characters) for _ in range(length))

class CustomFormatter(logging.Formatter):

	format = "%(asctime)s - %(levelname)s - %(message)s"

	FORMATS = {
		logging.DEBUG: Fore.WHITE + format + Fore.RESET,
		logging.INFO: Fore.CYAN + format + Fore.RESET,
		logging.WARNING: Fore.YELLOW + format + Fore.RESET,
		logging.ERROR: Fore.RED + format + Fore.RESET,
		# logging.ERROR: red + format + reset,
		logging.CRITICAL: Style.BRIGHT + Fore.RED + format + Fore.RESET + Style.NORMAL
	}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)

# class Log():
# 	def __self__(self, type, ):