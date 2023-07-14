#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
* @Author h3st4k3r
* @Version Mark.1
* Code designed to gather information from phishtank and upload it directly to MISP
* GNU General Public License
* This script is part of Hegemon's shadow project
*
"""
import requests
import HTTPHandler
from bs4 import BeautifulSoup

class phishtank():
    def __init__(self, misp_url, misp_key, misp_verifycert=False):
        # Objects
        self.misp_url = misp_url
        self.misp_key = misp_key
        self.misp_verifycert = misp_verifycert
        print("\n#########################\n\nStarting phishtank script\n\n#########################\n")

    def crawler(self):
        response = requests.get('https://phishtank.org/')
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        phishing_elements = soup.find_all('tr')
        for element in phishing_elements:
            td_elements = element.find_all('td')

            if len(td_elements) == 3:
                phishing_id = td_elements[0].find('a').text.strip()
                url = td_elements[1].text.strip()
                username = td_elements[2].find('a').text.strip()
                print(f"Phishing ID: {phishing_id}")
                print(f"URL: {url}")
                print(f"Username: {username}")
                print("---")
                event = {
                    "info":"Phishtank: "+str(url)
                }
                event_all = {
                    "info": "Phishtank: "+str(url),
                    "Attribute": [
                                  {"title": "Phishtank case: "+str(url)},
                                  {"description": "New phishing case on "+str(url)+" reported by "+str(username)+" ID Case "+str(phishing_id)},
                                  {"tags": ["phishing", "username", "url"]},
                                  { "threat_level": "LOW"},
                                  {"confidence": "LOW"},
                                  {"source": "PHISHTANK CRAWLER"},
                                  {"type": "Phishing"}
                    ]
                }

                response = HTTPHandler.HTTPHandler(self.misp_url, self.misp_key, self.misp_verifycert)

                if response.search_events(event):
                    print("El evento ya existe en MISP. No hago nada.")
                else:
                    print("El evento no existe en MISP.")
                    response.add_event(event_all)

    def run(self):
        self.crawler()
        print("#########################")

if __name__ == '__main__':
    pass
