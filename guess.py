import difflib
from argparse import ArgumentParser
from typing import Set

import requests
from colorama import Fore, Style


def banner() -> None:
	print(f"""{Fore.GREEN + Style.BRIGHT}
					  _ _
  ___ _ __ ___   __ _(_) |       __ _ _   _  ___  ___ ___  ___ _ __
 / _ \ '_ ` _ \ / _` | | |_____ / _` | | | |/ _ \/ __/ __|/ _ \ '__|
|  __/ | | | | | (_| | | |_____| (_| | |_| |  __/\__ \__ \  __/ |
 \___|_| |_| |_|\__,_|_|_|      \__, |\__,_|\___||___/___/\___|_|
								 |___/

	{Fore.RED + Style.BRIGHT}147 151 164 150 165 142 056 143 157 155 057 071 163 166

	{Fore.RESET}""")

hastebin = lambda data: "https://hastebin.com/" + (requests.post("https://hastebin.com/documents", data='\n'.join(data)).json().get("key"))

def download_domains() -> None:
	global email_domains
	with requests.get('https://raw.githubusercontent.com/IRIS-Team/IRIS/main/data/domains.txt') as request:
		email_domains = [x.strip() for x in request.text.splitlines() if len(x.strip()) > 0]

def __validate_guess__(email_domain: str, domain: str) -> bool:
		if len(email_domain) != len(domain):
			return False
		positions = []
		[positions.append((position, char)) for position, char in enumerate(email_domain) if char != '*']
		for position, char in positions:
			if domain[position] != char:
				return False
		return True

def guess_domain(email: str) -> Set[str]:
	email_user, email_domain = email.split('@')
	valid_matches = [str(email_user + '@' + domain) for domain in email_domains if __validate_guess__(email_domain, domain) is True]
	export = bool(len(difflib.get_close_matches(str(input("Would you like to save these results to a hastebin? ")), ['yes', 'y'])) >= 1)
	if export:
		return set([hastebin(valid_matches),])
	else:
		return valid_matches

def main() -> None:
	banner()
	download_domains()

	parser = ArgumentParser(epilog=f"{Fore.LIGHTRED_EX + Style.BRIGHT} --> github.com/9sv{Fore.RESET}")
	parser.add_argument("email", help="The email to guess")
	args = parser.parse_args()
	
	[print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}--> {Fore.LIGHTGREEN_EX + Style.BRIGHT}{domain}{Fore.RESET}\n") for domain in guess_domain(args.email)]

if __name__ == "__main__":
	main()
