# Phishkiller

## Overview
This script is designed to combat phishing attacks by flooding phisher databases with false information by flooding attacker database.

## How It Works
Using multi-threading, the script generates random email addresses and passwords from a predefined list of names. Each thread independently sends POST requests to a specified URL, submitting fictitious data to overwhelm phisher databases. This proactive approach aims to dilute and disrupt the accuracy of stolen data, offering a layer of protection to potential victims.

## Purpose
Stop phishing

## Phishkiller usage
Run 
```
pip install -r requirements.txt

python3 phishkiller.py --url {url} --threads {int}
 ```
 ## To Do List

 - Proxy (rotate IP address)
 - Logging
 - Input sanitization
 - Add Python Docstrings

 ### Disclaimer
**Note:** This script should be used responsibly and only on systems you have explicit permission to test against.
