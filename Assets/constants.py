from colorama import Fore, Back, Style
fields = ["email", "password", "username"]
EMPTY_FIELDS_ERROR = F"{Style.BRIGHT}{Fore.RED}[!] At least one field is required.{Fore.RESET}"
