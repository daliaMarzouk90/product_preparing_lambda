import json
from Config import settings
import requests
import logging
import sys
from math import ceil

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

class DataRetrival:
    def __init__(self, lang, products_ids, lang):
        self.lang = lang
        self.product_endpoint = settings["DB_ENDPOINT"].format(lang)+"products"
        self.compose_request_query(products_ids)
        self.total_count = self.get_docs_total_count()

    def compose_request_query(self, products_ids):
        self.base_query_string = "?searchCriteria[currentPage]={}&searchCriteria[pageSize]={}"

        self.base_query_string += "&searchCriteria[filter_groups][1][filters][0][field]=entity_id"
        
        self.base_query_string += "&searchCriteria[filter_groups][1][filters][0][value]={}".format(str(products_ids).replace(" ","").replace("\"", "")[1:-1])
        
        self.base_query_string += "&searchCriteria[filter_groups][1][filters][0][conditionType]=in"

    def get_docs_total_count(self):
        response = None
        
        try:
            response = self.make_request(1, 1)
        except Exception as e:
            logging.error(e)
            print(e)
            return 0

        return response["total_count"]

    def get_prducts_data(self, products_ids):
        page = 1

        if self.total_count <= 0:
            return []

        items = []

        while((page-1)*300 <= self.total_count):
            #1- make request
            response = self.make_request(page, 300)
        
            #2- extract data
            items += response["items"]

            if(len(items) > 0):
                page += 1

        return items
        
    def make_request(self, page, count):
        #response = None
        url = self.product_endpoint + self.base_query_string.format(page, count)

        logging.info("to hit {}".format(url))

        response = requests.get(url)

        try:
            response = response.text.encode("utf-8")
            return json.loads(response)
        except Exception as e:
            logging.error(e)
            return {"items": [], "total_count": 0}