import json
from Controller import product_preparing_controller

def lambda_handler(event, context):
    # TODO implement
    print("****************Start*****************************")
    products_ids = []
    for record in event["Records"]:
        record_products_ids = list(set(int(x["product_id"]) for x in json.loads(record["body"])))
        products_ids += record_products_ids

    product_preparing_controller.run("ar", products_ids)
    product_preparing_controller.run("en", products_ids)
    
    print("****************End*****************************")
    return {
        'statusCode': 200,
        'body': json.dumps('Product Preparing Lambda Finished!')
    }