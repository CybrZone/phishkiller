
import requests

def validate_url(base_url):
    """
    Validates a given base URL by checking if it is reachable via both HTTP and HTTPS protocols.

    Args:
        base_url (str): The base URL to validate.

    Returns:
        str: The validated URL with the appropriate protocol, or None if the URL is not reachable.
    """
    for protocol in ["https://", "http://"]:
        url = protocol + base_url
        try:
            response = requests.post(url, timeout=5)
            if response.status_code == 200:
                return url
        except requests.RequestException:
            continue
    return None
