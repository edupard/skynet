from google.cloud import logging
client = logging.Client()

def log(text):
    print(text)
    logger = client.logger("skynet")
    logger.log_text(text)