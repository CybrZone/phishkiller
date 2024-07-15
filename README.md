# PhishKiller
Creator: [CybrZone](https://github.com/CybrZone)

## Overview

PhishKiller is a Python script designed to disrupt phishing attacks by flooding phisher databases with false information. This proactive approach aims to protect potential victims from identity theft and fraud.

## How It Works

PhishKiller utilizes multi-threading to generate random email addresses and passwords. Each thread independently sends POST requests to specified URLs, submitting fictitious data to overwhelm phisher databases and dilute the accuracy of stolen information.

## Purpose

The primary goal of PhishKiller is to combat phishing attacks by flooding attacker databases with false information, thereby safeguarding potential victims and disrupting malicious operations.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CybrZone/phishkiller
   cd PhishKiller
2. **install dependencies:**

    ```bash
    pip install -r requirements.txt

## Usage

+ Run the script:

    ```bash
    python3 run.py
    
Follow the prompts to enter the URL of the target phishing site.

## Recent Improvements

+ **CLI Interface**: Enhanced user interaction with a *command-line interface* for streamlined operation.
+ **CONTRIBUTING and README**: Added CONTRBUTING and modified the Readme.
+ **Advanced Error Handling**: Implemented robust error handling to manage network and data processing errors effectively.
+ **Logging Configuration**: Improved logging setup for better traceability and debugging capabilities.
+ **Code Refactoring and Organization**: Restructured code into modules for improved maintainability.
+ **Enhanced Data Generation**: Improved algorithms for generating realistic email addresses and passwords.

# Recent Contributions

## Recent contributions have been made by:

+ [Harry James Green](https://github.com/HarryJamesGreen): Improved logging configuration.
+ [B1GBOOM420](https://github.com/B1GBOOM420): Enhanced data generation algorithms.
+ [LP-Pinkk](https://github.com/lp-pinkk): Contributed to project documentation and licensing.
+ [Mela-nen](https://github.com/lp-pinkk): Refactored codebase for better organization and readability.
+ [Ashesh Jyoti](https://github.com/asheshjyotii): Enhanced CLI interface, error handling, logging, added banner logo and real-time top contributor display; improved interface design and user-friendliness; updated README for usability, added CONTRIBUTING for contributors.

# Contributing
Contributions are welcome! Please check out our [CONTRIBUTING.md](https://github.com/CybrZone/phishkiller/blob/main/CONTRIBUTING) for guidelines on how to contribute to the project.

# License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/CybrZone/phishkiller/blob/main/LICENSE) file for details.

# Disclaimer

**Note**: This code is for educational and testing purposes only. It should not be used for any malicious or illegal activities. Using this code for unauthorized purposes may violate the terms of service of the target website and local/international laws. The use of this code is entirely at your own risk, and the authors/contributors are not responsible for any misuse or consequences arising from its use.
