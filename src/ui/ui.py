import requests
import json
from rich.console import Console

console = Console()

# ASCII logo as a multi-line string
logo_text = """
█▀█ █░█ █ █▀ █░█
█▀▀ █▀█ █ ▄█ █▀█

█▄▀ █ █░░ █░░ █▀▀ █▀█
█░█ █ █▄▄ █▄▄ ██▄ █▀▄"""

def show():
    """
    Display the ASCII logo and welcome message.
    """
    console.print(logo_text + "\n\n", justify="center")
    console.rule("[bold]Welcome to [bold][green]Phish Killer[/green][/bold]")
    console.print("[yellow]Top Maintainers\n", justify="center")

def contrib():
    """
    Fetch and display the top 5 contributors from the GitHub repository.
    Fallback to local JSON file if GitHub API request fails.
    """
    owner = "CybrZone"
    repo = "phishkiller"
    contrib_dict = {}

    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        contributors_full_info = response.json()

        for x in contributors_full_info:
            contrib_dict[x['login']] = x['contributions']

        with open('src/utils/contrib.json', 'w') as f:
            json.dump(contrib_dict, f)

        display_contributors(contrib_dict)

    except requests.exceptions.RequestException:
        console.print("Failed to fetch contributors from GitHub. Loading local data...", style="bold yellow")
        load_local_contributors()

def load_local_contributors():
    """
    Load and display contributors from the local JSON file.
    """
    try:
        with open('src/utils/contrib.json', 'r') as f:
            contrib_dict = json.load(f)
            display_contributors(contrib_dict)
    except FileNotFoundError:
        console.print("No local data found. Please check your internet connection.", style="bold red")
    except json.JSONDecodeError:
        console.print("Error decoding JSON from the local file.", style="bold red")

def display_contributors(contrib_dict):
    """
    Display the top 5 contributors.
    """
    count = 0
    for key, value in contrib_dict.items():
        console.print(f"🔱 {key} 🔱", justify="center")
        count += 1
        if count >= 5:
            break

if __name__ == "__main__":
    show()
    contrib()
