from lambda_function import lambda_handler
import json

events = None
events = {"Records": [{"body": 35643}, {"body": 345}, {"body": 0000000}]}

lambda_handler(events, {})