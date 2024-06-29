#!/usr/bin/env python3
# https://github.com/leolion3/Portfolio/tree/master/Python/GmailPermutationGenerator
from sys import argv
from itertools import permutations, product
from typing import List


suffixes = ['@gmail.com', '@googlemail.com']


def generate_dot_positions(word: str, num_dots: int) -> List[List[int]]:
	"""
	Generates all permutations for inserting dots between letters.
	Generates duplicate dots too - Bug/Feature?
	"""
	word_length = len(word)
	positions = list(permutations(range(1, word_length), num_dots))
	valid_positions = []
	for pos in positions:
		valid = True
		for i in range(len(pos) - 1):
			if pos[i] + 1 == pos[i + 1]:
				valid = False
				break
		if valid:
			valid_positions.append(list(pos))
	return valid_positions


def add_dots_to_string(word: str, dot_positions: List[List[int]]) -> List[str]:
	"""
	Adds dots to a word at given dot positions.
	"""
	dotted_words = []
	for positions in dot_positions:
		dotted_word = list(word)
		for pos in positions:
			dotted_word.insert(pos, '.')
		dotted_word = ''.join(dotted_word)
		if '..' in dotted_word:
			continue
		dotted_words.append(dotted_word)
	return sorted(list(set(dotted_words)))


def add_suffixes(permutated: List[str], suffixes: List[str], service: str) -> List[str]:
	"""
	Adds email suffixes and service to permutated usernames.
	"""
	usernames = []
	if len(service):
		permutated = [f'{x}+{service}' for x in permutated]
	for suffix in suffixes:
		usernames.extend([f'{x}{suffix}' for x in permutated])
	return usernames


def generate_character_permutations(username: str) -> List[str]:
	"""
	Generates uppercase/lowercase permutations for given username.
	"""
	perms = set()
	for chars in product(*zip(username.lower(), username.upper())):
		permutation = ''.join(chars)
		if permutation != username:
			perms.add(permutation)
	return list(perms)


def generate_permutations(username: str, charcase: bool) -> List[str]:
	generated = []
	permutated_usernames = [username]
	if charcase:
		permutated_usernames = generate_character_permutations(username)
	for i in range(1, 2):
		p = generate_dot_positions(username, i)
		for s in permutated_usernames:
			dotted = add_dots_to_string(s, p)
			generated.extend(dotted)
	return sorted(list(set(generated)))


def write_entries(generated: List[str], filename: str) -> None:
	print(f'{len(generated)} Permutations generated, caching to {filename}...')
	print('Permutations:')
	with open(export_file_name, 'a+') as f:
		for entry in generated:
			print(f'- {entry}')
			f.write(f'{entry}\n')
		f.flush()
	print(f'Permutations exported to {filename}')


if __name__ == '__main__':
	if len(argv) < 2:
		print('Generates email permutations for a given username and service (Netflix, for instance).')
		print(f'Usage: {argv[0]} username <charcase(True/False)> [service] [export_file_name]')
		exit()

	username = argv[1]
	charcase = False

	if len(argv) > 2:
		if 't' in argv[2].lower():
			charcase = True

	service = ''
	if len(argv) > 3:
		service = argv[3]

	export_file_name = 'export.txt'
	if len(argv) > 4:
		export_file_name = argv[4]

	generated = add_suffixes(generate_permutations(username, charcase), suffixes, service)
	write_entries(generated, export_file_name)
	