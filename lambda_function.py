import json
from Controller import product_preparing_controller

def lambda_handler(event, context):
    # TODO implement
    print("****************Start*****************************")
    

    product_preparing_controller.run("ar", [x["body"] for x in event["Records"]])
    
    print("****************End*****************************")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }