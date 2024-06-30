# Phishkiller

## Overview

PhishKiller is a Python script designed to flood phishing website's databases with fake login data to disrupt their malicious activities.

## How It Works - Features

- Generates random email addresses and passwords.
- Uses asynchronous requests for high performance.
- Randomizes User-Agent headers to avoid detection.
- Structured logging for monitoring activities.
- Handles errors gracefully.

## Purpose
Providing easy access to a script any whitehat can use to stop phishing.

## Installation
1. Clone the Repository:
```
git clone https://github.com/musprodev/phishkiller.git
cd phishkiller
```
2. Install dependencies using **pip**:
```
pip install -r requirements.txt
```

## Phishkiller usage

1. **Run** 
```
python3 phishkiller.py
 ```
2. Follow the prompts to enter the URL of the phishing link you want to target and the number of POST requests to send.
3. Monitor the console/terminal for logging messages that track the script's progress and status.

> The script uses structured logging with timestamps (%(asctime)s), log levels (%(levelname)s), and messages (%(message)s). Logs are output in the console to track each POST request's status and details.

## To Do List

 - Proxy (rotate IP address)

## Contributing

Contributions are welcome! If you find bugs or want to add features, please fork the repository and submit a pull request.

 ### Disclaimer
**Note:** This script should be used responsibly and only on systems you have explicit permission to test against (controlled environment). 

*A testserver `pytestserver.py` has been made available to simulate a real phishing page to test the script*
