import logging
import os

def setup_logging(log_file='app.log', log_level=logging.INFO):
    """
    Sets up logging for the application.

    Args:
        log_file (str): The name of the log file. Defaults to 'app.log'.
        log_level (int): The logging level. Defaults to logging.INFO.
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_path = os.path.join('logs', log_file)

    # Configure the logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
        ]
    )

    # Set up logging for external libraries if needed
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

# Example usage
if __name__ == "__main__":
    setup_logging()
    logging.info("Logging setup complete.")
