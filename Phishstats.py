#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
* @Author h3st4k3r
* @Version Mark.1
* Code designed to gather information from phishstats and upload it directly to MISP
* GNU General Public License
* This script is part of Hegemon's shadow project
*
"""
import requests
import HTTPHandler

class phishstats():
    def __init__(self,misp_url, misp_key, misp_verifycert=False):
        # Objects
        self.misp_url = misp_url
        self.misp_key = misp_key
        self.misp_verifycert = misp_verifycert
        print("\n#########################\n\nStarting phishtats script\n\n#########################\n")

    def make_request(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return "error"

    def get_latest_phishings(self):
        return self.make_request("https://phishstats.info:2096/api/phishing?_sort=-id&_size={20}")

    def run(
            self):
        latest_phishings = self.get_latest_phishings()
        if latest_phishings:
            for phishing in latest_phishings:
                id= phishing["id"]
                url=phishing["url"]
                ip=phishing["ip"]
                hash=phishing["hash"]
                print(str(url))
                print("---")
                event = {
                    "info": "Phishstats: " + str(url)
                }
                event_all = {
                    "info": "Phishstats: " + str(url),
                    "Attribute": [
                        {"title": "Phishstats case: " + str(url)},
                        {"description": "New phishing case on " + str(url) + "IP: "+ str(ip) + " ID Case " + str(id) + "Hash: "+ hash},
                        {"tags": ["phishing", "url"]},
                        {"threat_level": "LOW"},
                        {"confidence": "LOW"},
                        {"source": "PHISHSTATS CRAWLER"},
                        {"type": "Phishing"}
                    ]
                }
                response = HTTPHandler.HTTPHandler(self.misp_url, self.misp_key, self.misp_verifycert)

                if response.search_events(event):
                    print("El evento ya existe en MISP. No hago nada.")
                else:
                    print("El evento no existe en MISP.")
                    response.add_event(event_all)

        print("#########################")


if __name__ == '__main__':
    pass
