from google.cloud import pubsub_v1
import abstraction.gcp_constants as constants

subscriber = pubsub_v1.SubscriberClient()

batch_settings = pubsub_v1.types.BatchSettings(max_bytes=1024, max_latency=1)
publisher = pubsub_v1.PublisherClient(batch_settings)


def pull_job_queue_items(queue_name, max_batch_size, ack_immediatelly, processor):
    subscription_path = subscriber.subscription_path(constants.PROJECT_NAME, queue_name)
    response = subscriber.pull(subscription_path, max_messages=max_batch_size)
    ack_ids = []
    messages = []
    def ack():
        print(f'Ack {len(response.received_messages)} {queue_name} job queue messages')
        subscriber.acknowledge(subscription_path, ack_ids)

    for received_message in response.received_messages:
        messages.append(received_message.message.data)
        ack_ids.append(received_message.ack_id)

    num_messages = len(messages)
    print(f'Received {num_messages} {queue_name} job queue messages')
    if ack_immediatelly:
        ack()
    processor.Process(messages)
    if not ack_immediatelly:
        ack()
    return num_messages

def push_job_queue_items(topic_name, messages):
    topic_path = publisher.topic_path(constants.PROJECT_NAME, topic_name)
    futures = []
    for m in messages:
        # Data must be a bytestring
        data = m.encode("utf-8")
        future = publisher.publish(topic_path, data)
        futures.append(future)

    for f in futures:
        f.result()
    print(f"published {len(messages)} to {topic_name} topic")
