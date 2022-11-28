import json
from Controller import product_preparing_controller

def lambda_handler(event, context):
    # TODO implement
    print("****************Start*****************************")
    
    products_ids = [int(x["body"]["product_id"]) for x in event["Records"]]
    product_preparing_controller.run("ar", products_ids)
    product_preparing_controller.run("en", products_ids)
    
    print("****************End*****************************")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }