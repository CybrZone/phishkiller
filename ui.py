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
    # Print logo
    console.print(logo_text + "\n\n", justify="center")
    # Print Welcome
    console.print("[bold]Welcome to [bold][green]Phish Killer\n", justify="center")
    # Print creator
    console.print("[yellow]Top Maintainers\n", justify="center")

def contrib():
    # Repo creator details
    owner = "CybrZone"
    repo = "phishkiller"
    contrib_dict = {}
    
    # GitHub API URL for contributors
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    
    # Make a request to the GitHub API
    response = requests.get(url)
    
    # Check if the request is successful
    if response.ok:
        contributors_full_info = response.json()
        # Update list of contributors
        for x in contributors_full_info:
            contrib_dict[x['login']] = x['contributions']
        
        # Write contributors to a JSON file
        with open('contrib.json', 'w') as f:
            json.dump(contrib_dict, f)

        count = 0
        # Print contributors, up to 5
        for key, value in contrib_dict.items():
            console.print(f"🔱 {key} 🔱", justify="center")
            count += 1
            if count >= 5:
                break
    else:
        console.print("Failed to fetch contributors.", justify="center")