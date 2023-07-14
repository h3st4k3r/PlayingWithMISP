# PlayingWithMISP
A crud to work with the MISP API, different information gathering crawlers oriented to upload new events in MISP, automatic report generation...
# Usage
If you want you can generate a main.py with this code:

"""
!/usr/bin/env python
-*- coding: utf-8 -*-
* @Author h3st4k3r
* @Version Mark.1
"""

import Phishtank
import Phishstats
import Autoreports

if __name__ == '__main__':
    misp_url = 'your_misp_url'
    misp_key = 'your_api_key'
    phishtank_module = Phishtank.phishtank(misp_url, misp_key)
    phishtank_module.run()
    #phishtstats_module = Phishstats.phishstats()
    #phishtstats_module.run()
    #events_to_report=5
    #autoreports_module = Autoreports.Reporting(misp_url, misp_key,events_to_report)
    #autoreports_module.run()

Then run with: python3 main.py
