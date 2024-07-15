import threading  # For multi-threading support
import os  # For accessing CPU count
import requests  # For making HTTP requests
import beaupy  # For CLI prompts and interactions
from src.ui.ui import show, contrib, console  # UI functions
from src.attack.attack import send_posts, hit  # Attack functions
from src.config.loggingConfig import setup_logging  # Logging setup
from src.utils.validators import validate_url  # URL validation function

def handle_user_input():
    """Handles user input to determine action."""
    return beaupy.prompt(
        prompt="[bright_cyan]🏮 [bold]Enter '1'[/bold] to [underline]attack a phishing site[/underline][/bright_cyan] \n[bright_red]🏮 [bold]Enter '0'[/bold] to [underline]Exit the tool[/underline].[/bright_red]",
        target_type=str,
        validator=lambda input: len(input) > 0,
        secure=False,
        raise_validation_fail=True,
        raise_type_conversion_fail=True,
        initial_value=None,
        completion=None
    )

def handle_target_url():
    """Handles user input for the target phishing site URL."""
    return beaupy.prompt(
        prompt="[bright_cyan]🔗 [bold]Enter the phishing site link:[/bold][/bright_cyan]",
        target_type=str,
        validator=lambda input: len(input) > 0,
        secure=False,
        raise_validation_fail=True,
        raise_type_conversion_fail=True,
        initial_value=None,
        completion=None
    )

def handle_number_of_posts():
    """Handles user input for the number of attack posts."""
    return int(beaupy.prompt(
        prompt="[bright_cyan]💥 [bold]Enter number of attacks to perform:[/bold][/bright_cyan] 💥\n[bright_red]   (enter only '0' to exit)[/bright_red]",
        target_type=int,
        validator=lambda input: input >= 0,
        secure=False,
        raise_validation_fail=False,
        raise_type_conversion_fail=True,
        initial_value=None,
        completion=None
    ))

def main():
    """Main function to orchestrate the phishing attack."""
    setup_logging()  # Initialize logging configuration
    show()  # Display initial UI
    contrib()  # Display contributors
    console.rule("")  # Print a console rule for separation
    
    user_input = handle_user_input()  # Get user's choice
    
    if int(user_input) == 1:  # If user chooses to attack
        target_url = handle_target_url()  # Get target URL
        
        # Validate and normalize the target URL
        if not (target_url.startswith('http://') or target_url.startswith('https://')):
            target_url = validate_url(target_url)
            if not target_url:
                print("Unable to reach the site with both http and https.")
                console.print("[green]PhishKiller[/green] [bold red]closed 🛑[/bold red]")
                exit()

        number_of_posts = handle_number_of_posts()  # Get number of attack posts
        if number_of_posts == 0:
            console.print("[green]PhishKiller[/green] [bold red]closed 🛑[/bold red]")
            exit()

        num_threads = os.cpu_count() or 4  # Get CPU count or default to 4
        posts_per_thread = number_of_posts // num_threads  # Posts per thread
        remainder = number_of_posts % num_threads  # Remaining posts

        hit_lock = threading.Lock()  # Lock for hit count
        threads = []

        # Create and start threads for performing attacks
        for i in range(num_threads):
            thread_posts = posts_per_thread + (1 if i < remainder else 0)
            thread = threading.Thread(target=send_posts, args=(target_url, thread_posts, hit_lock), daemon=True)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        console.print(f"\n[bright_magenta]🚀 [bold]Total successful hits:[/bold][/bright_magenta] [bright_cyan]{hit[0]}[bright_cyan]\n")

    else:  # If user chooses to exit
        console.print("[green]PhishKiller[/green] [bold red]closed 🛑[/bold red]")

if __name__ == "__main__":
    main()
