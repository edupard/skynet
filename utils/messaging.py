from google.cloud import pubsub_v1

import utils.constants as constants


class Subscriber():

    def __init__(self):
        self.client = pubsub_v1.SubscriberClient()

    def ack(self, queue_name, to_ack):
        subscription_path = self.client.subscription_path(constants.PROJECT_NAME, queue_name)
        self.client.acknowledge(subscription_path, to_ack)

    def pull_messages(self, queue_name, max_batch_size):
        subscription_path = self.client.subscription_path(constants.PROJECT_NAME, queue_name)
        response = self.client.pull(subscription_path, max_messages=max_batch_size, return_immediately=True)
        ack_ids = []
        messages = []

        for received_message in response.received_messages:
            messages.append(received_message.message.data.decode("utf-8"))
            ack_ids.append(received_message.ack_id)

        return messages, ack_ids


class Publisher():
    def __init__(self):
        batch_settings = pubsub_v1.types.BatchSettings(max_bytes=1024, max_latency=1)
        self.client = pubsub_v1.PublisherClient(batch_settings)

    def send_messages(self, queue_name, messages):
        topic_path = self.client.topic_path(constants.PROJECT_NAME, queue_name)
        futures = []
        for m in messages:
            # Data must be a bytestring
            data = m.encode("utf-8")
            future = self.client.publish(topic_path, data)
            futures.append(future)

        for f in futures:
            f.result()
