# PlayingWithMISP

This repository contains a CRUD (Create, Read, Update, Delete) application that interacts with the MISP (Malware Information Sharing Platform) API. It also includes different information gathering crawlers designed to upload new events to MISP and an automatic report generation feature.

## Usage

To use the application, follow these steps:

1. Create a `main.py` file with the following code:

#!/usr/bin/env python

-- coding: utf-8 --
"""
Author: h3st4k3r
Version: Mark.1
"""

import Phishtank
import Phishstats
import Autoreports

if name == 'main':
misp_url = 'your_misp_url'
misp_key = 'your_api_key'
phishtank_module = Phishtank.phishtank(misp_url, misp_key)
phishtank_module.run()
phishstats_module = Phishstats.phishstats()
phishstats_module.run()
events_to_report = 5
autoreports_module = Autoreports.Reporting(misp_url, misp_key, events_to_report)
autoreports_module.run()


Make sure to replace `'your_misp_url'` with the URL of your MISP instance and `'your_api_key'` with your MISP API key. Uncomment the relevant lines according to the modules you want to run.

2. Run the application by executing the following command in your terminal: `python3 main.py`

This will execute the specified modules, interacting with the MISP API based on the provided configuration.

Feel free to customize the code and enable additional modules according to your needs. Make sure you have the required dependencies installed before running the application.

## Modules

### Phishtank

The `Phishtank` module is designed for gathering phishing URLs from the Phishtank API and uploading new events to MISP for further analysis.

### Phishstats

The `Phishstats` module is designed to gather phishing URLs from the Phishstats API and upload them to MISP.

### Autoreports

The `Autoreports` module (currently commented out in the code) generates automatic reports based on a specified number of events in MISP. These reports can be used for analysis or sharing with other users.

## Requirements

- Python 3.x
- Dependencies:
  - `pymisp`: Python library for interacting with the MISP API (Install with `pip install pymisp`)
  - requests: Library for making HTTP requests (Install with `pip install requests`)
  - beautifulsoup4: Library for web scraping (Install with `pip install beautifulsoup4`)
  - Additional dependencies may be required based on the specific modules used.
