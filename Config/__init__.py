
import os

def __extract_configurations():
    settings = {}

    settings["DB_ENDPOINT"] = os.getenv("DB_ENDPOINT")
    settings["AWS_ACCESS_KEY_ID"] = os.getenv("ACCESS_KEY_ID")
    settings["AWS_SECRET_ACCESS_KEY"] = os.getenv("SECRET_ACCESS_KEY")
    settings["AWS_REGION"] = os.getenv("REGION")

    settings["EN_SQS_NAME"] = os.getenv("EN_SQS_NAME")
    settings["AR_SQS_NAME"] = os.getenv("AR_SQS_NAME")

    return settings

settings = __extract_configurations()