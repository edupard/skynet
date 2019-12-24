from google.cloud import pubsub_v1
import abstractions.gcp_constants as constants

subscriber = pubsub_v1.SubscriberClient()

batch_settings = pubsub_v1.types.BatchSettings(max_bytes=1024, max_latency=1)
publisher = pubsub_v1.PublisherClient(batch_settings)

def ack(queue_name, to_ack):
    subscription_path = subscriber.subscription_path(constants.PROJECT_NAME, queue_name)
    subscriber.acknowledge(subscription_path, to_ack)

def pull_job_queue_items(queue_name, max_batch_size):
    subscription_path = subscriber.subscription_path(constants.PROJECT_NAME, queue_name)
    response = subscriber.pull(subscription_path, max_messages=max_batch_size)
    ack_ids = []
    messages = []

    for received_message in response.received_messages:
        messages.append(received_message.message.data.decode("utf-8"))
        ack_ids.append(received_message.ack_id)

    return messages, ack_ids

def push_job_queue_items(queue_name, messages):
    topic_path = publisher.topic_path(constants.PROJECT_NAME, queue_name)
    futures = []
    for m in messages:
        # Data must be a bytestring
        data = m.encode("utf-8")
        future = publisher.publish(topic_path, data)
        futures.append(future)

    for f in futures:
        f.result()
