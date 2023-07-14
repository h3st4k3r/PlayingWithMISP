#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* @Author h3st4k3r
* @Version Mark.1
* CRUD designed to work with MISP
* GNU General Public License
* This script is part of Hegemon's shadow project
*
"""
from pymisp import ExpandedPyMISP

class HTTPHandler:

    def __init__(self, misp_url, misp_key, misp_verifycert):
        self.misp_url = misp_url
        self.misp_key = misp_key
        self.misp_verifycert = misp_verifycert
        self.misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert)

    def search_events(self, query):
        body = {"returnFormat": "json", "value": query["info"], "searchall": True}
        relative_path = 'events/restSearch'
        if self.misp.direct_call(relative_path, body):
            print(self.misp.direct_call(relative_path, body))
            return True
        else:
            return False

    def add_event(self, query):
        relative_path = 'events/add'
        response = self.misp.direct_call(relative_path, query)
        return response

    def get_event(self, event_id):
        relative_path = f'events/{event_id}'
        response = self.misp.direct_call(relative_path)
        event = response.get('Event', {})
        return event

    def delete_event(self, event_id):
        relative_path = f'events/delete/{event_id}'
        response = self.misp.direct_call(relative_path)
        return response
