# PlayingWithMISP

This repository contains a CRUD (Create, Read, Update, Delete) application that interacts with the MISP (Malware Information Sharing Platform) API. It also includes different information gathering crawlers designed to upload new events to MISP and an automatic report generation feature.

## Usage

To use the application, follow these steps:

1. Create a `main.py` file with the following code:

```python
import Phishtank
import Phishstats
import Autoreports
import ZoneH

if name == 'main':
  misp_url = 'your_misp_url'
  misp_key = 'your_api_key'
  events_to_report = 5
  phishtank_module = Phishtank.phishtank(misp_url, misp_key)
  phishtank_module.run()
  phishstats_module = Phishstats.phishstats()
  phishstats_module.run()
  autoreports_module = Autoreports.Reporting(misp_url, misp_key, events_to_report)
  autoreports_module.run()
  zoneh_module = ZoneH.ZoneHScraper(misp_url, misp_key)
  zoneh_module.run()
```

Make sure to replace `'your_misp_url'` with the URL of your MISP instance and `'your_api_key'` with your MISP API key. Uncomment the relevant lines according to the modules you want to run.

Or maybe, if you want, you can use the `config.ini` file:

```python
import Defacements
import Phishtank
import Phishstats
import Autoreports
import ZoneH
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == '__main__':
    misp_url = config.get('misp', 'url')
    misp_key = config.get('misp', 'key')
    misp_verifycert = config.getboolean('misp', 'verifycert')
    phishtank_module = Phishtank.phishtank(misp_url, misp_key)
    phishtank_module.run()
    phishtstats_module = Phishstats.phishstats(misp_url, misp_key)
    phishtstats_module.run()
    events_to_report=5
    autoreports_module = Autoreports.Reporting(misp_url, misp_key,events_to_report)
    autoreports_module.run()
    zoneh_module = ZoneH.ZoneHScraper(misp_url, misp_key)
    zoneh_module.run()
```

2. Run the application by executing the following command in your terminal: `python3 main.py`

This will execute the specified modules, interacting with the MISP API based on the provided configuration.

Feel free to customize the code and enable additional modules according to your needs. Make sure you have the required dependencies installed before running the application.

## Modules

### Phishtank

The `Phishtank` module is designed for gathering phishing URLs from the Phishtank API and uploading new events to MISP for further analysis.

### Phishstats

The `Phishstats` module is designed to gather phishing URLs from the Phishstats API and upload them to MISP.

### Autoreports

The `Autoreports` module generates automatic reports based on a date (one month ago) and based on a number (in this case 5). These reports can be used for analysis or sharing with other users.

### ZoneH

The `ZoneH`module is designed for gathering defacement in from ZoneH and upload it directly to MISP. In this case we use diferent User-Agents to evade captcha.
If you want to replace more User-Agents watch the `agents.md` file.

## Requirements

- Python 3.x
- Dependencies:
  - **pymisp**: Python library for interacting with the MISP API (Install with `pip install pymisp`)
  - **requests**: Library for making HTTP requests (Install with `pip install requests`)
  - **beautifulsoup4**: Library for web scraping (Install with `pip install beautifulsoup4`)
  - **Selenium:** Library for automating browser actions (Install with `pip install selenium`)
  - Additional dependencies may be required based on the specific modules used.
 
## Output from MISP

Here you can watch how we get information from Phishtank and Phishstats:

<img width="1160" alt="image" src="https://github.com/h3st4k3r/PlayingWithMISP/assets/40382991/d0777bba-32c4-4c88-a5d3-51b269774131">

And here you can watch how we get information from ZoneH:

<img width="999" alt="image" src="https://github.com/h3st4k3r/PlayingWithMISP/assets/40382991/c80f655a-c02d-43ba-a6ce-f64d69f9b056">


## Note

These crawlers can be run via cron to get the most out of them. In this way, we can ensure that we constantly obtain information in real time and without missing anything.
These scripts are for didactic purposes only; future enhancements will include implementations that leave the data normalised for MISP (watch: https://github.com/MISP/misp-playbooks/tree/main/documentation).

## Licence

This project is licensed under the GNU License.

