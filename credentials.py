#!/usr/bin/env python3
from loguru import logger
from faker import Faker
from itertools import permutations
import string
import random
from typing import List, Tuple


class CredentialGenerator:
	alphabet = string.ascii_letters + string.digits + string.punctuation
	domains = ['@googlemail.com', "@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"]
	fake = Faker()

	@staticmethod
	def add_suffixes(permutated: List[str], suffixes: List[str], service: str) -> List[str]:
	    """
	    Adds email suffixes and service to permutated usernames.
	    :param permutated: list of email permutation prefixes.
	    :param suffixes: list of email domains.
	    :param service: optional service - gmail allows adding + followed by string after username, ex. test+netflix@gmail.com
	    :return: email permutations with domain suffixes.
	    """
	    usernames = []
	    if len(service):
	        permutated = [f'{x}+{service}' for x in permutated]
	    for suffix in suffixes:
	        usernames.extend([f'{x}{suffix}' for x in permutated])
	    return usernames

	def generate_random_emails(self) -> List[str]:
	    """
	    Generates random email addresses.
	    :return: a list of generated (unique) emails
	    """
	    first  = self.fake.first_name().lower()
	    last = self.fake.last_name().lower()
	    middle = random.choice(['_', '.', ''])
	    emails = [random.choice([str(random.randint(1, 99)), '']) for _ in range(3)]
	    emails.extend([first, last, middle])
	    emails = list(filter(len, emails))
	    # Generate permutations
	    emails = list(set(permutations(emails)))
	    emails = [''.join(x) for x in emails]
	    # Add domains
	    return self.add_suffixes(emails, self.domains, '')

	def generate_random_password(self, max_len: int = 50) -> str:
	    """
	    Generate a random password up to the given max len.
	    :param max_len: maximum password length, default is 50.
	    :return: the generated password.
	    """
	    pw_len = random.randint(8, max_len)
	    return ''.join(random.choice(self.alphabet) for i in range(pw_len))

	def generate_credentials(self):
		mails = self.generate_random_emails()
		self.emails.extend(mails)
		for _ in range(len(mails)):
			self.passwords.append(self.generate_random_password())

	def buffered_generator(self) -> None:
		"""
		Continuous buffered generation of credentials, runs as independent thread.
		:return:
		"""
		while len(self.emails) < 50:
			self.generate_credentials()

	def get_credentials(self) -> Tuple[str, str]:
		"""
		Get a new email/password pair.
		:return: an email/password pair.
		"""
		while len(self.emails) < 25:
			self.generate_credentials()
		email = random.choice(self.emails)
		password = random.choice(self.passwords)
		self.emails.remove(email)
		self.passwords.remove(password)
		return email, password

	def __init__(self):
		self.emails: List[str] = []
		self.passwords: List[str] = []
