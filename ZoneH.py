#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
* @Author h3st4k3r
* @Version Mark.1
* Code designed to gather information from ZoneH and upload it directly to MISP
* GNU General Public License
* This script is part of Hegemon's shadow project
*
"""

import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import HTTPHandler

# Cambiamos el User-Agent en cada petición evitando que nos salte el captcha
# Si deseas añadir más user-agents puedes mirar el fichero agents.txt en este mismo repositorio.
class UserAgentChanger:
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]

    @staticmethod
    def get_random_user_agent():
        return random.choice(UserAgentChanger.USER_AGENTS)

# En esta clase realizamos el scraping del contenido de ZoneH
class ZoneHScraper:
    BASE_URL = 'https://www.zone-h.org/archive'

    def __init__(self, misp_url, misp_key, misp_verifycert=False):
        self.misp_url = misp_url
        self.misp_key = misp_key
        self.misp_verifycert = misp_verifycert
        self.user_agent_changer = UserAgentChanger()
        self.driver = self._initialize_driver()
        print("\n#########################\n\nStarting Zone-H script\n\n#########################\n")

    def _initialize_driver(self):
        options = Options()
        options.add_argument(f'user-agent={self.user_agent_changer.get_random_user_agent()}')
        driver = webdriver.Chrome(options=options)
        return driver

    def scrape_latest_defacements(self):
        url = f'{ZoneHScraper.BASE_URL}/filter=1'
        self.driver.get(url)
        time.sleep(5)  # Le damos un poco de tiempo para que cargue bien la página.

        table = self.driver.find_element(By.ID, 'ldeface')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        defacements = []
        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) >= 9:  # Coprobamos si hay suficientes celdas, esto evita errores en caso de no haber suficientes celdas.
                defacement_time = cells[0].text
                notifier = cells[1].text
                domain = cells[7].text
                os = cells[8].text
                defacements.append({'time': defacement_time, 'notifier': notifier, 'domain': domain, 'os': os})
        return defacements

    def close(self):
        self.driver.quit()

    def run(self):
        defacements = self.scrape_latest_defacements()
        for defacement in defacements:
            formatted_defacement = f"Time: {defacement['time']}; Notifier: {defacement['notifier']}; Domain: {defacement['domain']}; OS: {defacement['os']}"
            print(formatted_defacement)
            domain=defacement['domain']
            notifier=defacement['notifier']

            event = {
                "info": "ZONE-H case: " + domain
            }

            event_all = {
                "info": "ZONE-H case: " + domain,
                "Attribute": [
                    {"title": "ZONE-H case: " + domain},
                    {"description": f"New Zone-H case on "+ domain +" notified by "+ notifier},
                    {"tags": ["defacement", "url"]},
                    {"threat_level": "HIGH"},
                    {"confidence": "HIGH"},
                    {"source": "ZONEH CRAWLER"},
                    {"type": "ZONEH"}
                ]
            }

            response = HTTPHandler.HTTPHandler(self.misp_url, self.misp_key, self.misp_verifycert)
            if response.search_events(event):
                print("El evento ya existe en MISP. No se hace nada.")
            else:
                print("El evento no existe en MISP. Se añade el evento.")
                response.add_event(event_all)
            self.close()


if __name__ == '__main__':
    pass
