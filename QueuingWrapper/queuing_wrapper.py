import boto3
from botocore.exceptions import ClientError

import json

from Config import settings

queue = None

class SQSWrapper:
    def __init__(self, lang) -> None:
        if lang == "en":
            sqs_name = settings["EN_SQS_NAME"]
        else:
            sqs_name = settings["AR_SQS_NAME"]
            
        sqs = boto3.resource('sqs',
                    aws_access_key_id = settings["AWS_ACCESS_KEY_ID"],
                    aws_secret_access_key = settings["AWS_SECRET_ACCESS_KEY"],
                    region_name = settings["AWS_REGION"]
                    )

        self.queue = sqs.get_queue_by_name(QueueName=sqs_name)

    def write_message(self, message):
        pass

    def write_bulk_messages(self, messages):

        for start_idx in range(0, len(messages), 10):
            self.queue.send_messages(QueueUrl=self.queue.url,
                                        Entries=[{"Id": str(x["body"]["id"]),"MessageBody": json.dumps(x) } for x in messages[start_idx:start_idx+10]])