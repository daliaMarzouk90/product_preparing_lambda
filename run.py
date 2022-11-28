from lambda_function import lambda_handler
import json

events = None
events = {"Records": [{"body": {"product_id":"104"}}, {"body": {"product_id":"345"}}, {"body": {"product_id":"0000000"}}]}


lambda_handler(events, {})