import boto3
from botocore.exceptions import ClientError

import json

from Config import config

queue = None




class SQSWrapper:
    def __init__(self) -> None:
        sqs = boto3.resource('sqs',
                    aws_access_key_id = config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY,
                    region_name = config.AWS_REGION
                    )

        self.queue = sqs.get_queue_by_name(QueueName=config.SQS_NAME)

    def write_message(self, message):
        pass

    def write_bulk_messages(self, messages):

        for start_idx in range(0, len(messages), 10):
            self.queue.send_messages(QueueUrl=self.queue.url,
                                        Entries=[{"Id": str(x["body"]["id"]),"MessageBody": json.dumps(x) } for x in messages[start_idx:start_idx+10]])