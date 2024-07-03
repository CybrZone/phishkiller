# Phishkiller

## Overview
This script is designed to combat phishing attacks by flooding phisher databases with false information by flooding attacker database.

## How It Works
Using multi-threading, the script generates random email addresses and passwords from a predefined list of names. Each thread independently sends POST requests to a specified URL, submitting fictitious data to overwhelm phisher databases. This proactive approach aims to dilute and disrupt the accuracy of stolen data, offering a layer of protection to potential victims.

## Purpose
Stop phishing


## Phishkiller usage

### Optional
To hide your ip (you're not safe from feds, but you won't get blocked by the site) you can add proxies to the proxies.txt file. The format is: protocol://(username:password)@ip:port. If you want free premium proxies check out webshare.io (not sponsored, but you get 10 premium proxies for free without a cc)

### Mandatory
Run
```
python3 phishkiller.py
 ```
 Then paste the url of the target and add the fields.


 ## To Do List

 - Get method
 - Checking and removing broken proxies
 - Automated proxy collection

 ### Disclaimer
**Note:** This script should be used responsibly and only on systems you have explicit permission to test against.
