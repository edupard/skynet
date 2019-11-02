import pika
from functools import partial
from config import get_config
from queue import Queue
import threading

def _get_connection_parameters():
    config = get_config()
    credentials = pika.PlainCredentials(config.RMQ_UNM, config.RMQ_PWD)
    return pika.ConnectionParameters(config.RMQ_HOST,
                                           config.RMQ_PORT,
                                           '/',
                                           credentials)

def _get_blocking_rmq_connection():
    parameters = _get_connection_parameters()
    return pika.BlockingConnection(parameters)

def publish_strings(messages, exchange, routing_key):
    connection = _get_blocking_rmq_connection()
    channel = connection.channel()

    for m in messages:
        body = m.encode()
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)

    connection.close()

class StoppedFlag:
    stopped = False

    def is_stopped(self):
        return self.stopped

    def stop(self):
        self.stopped = True

class HandlerInfo(object):
    PrefetchCount = None
    Handler = None
    def __init__(self, prefetchCount, handler):
        self.PrefetchCount = prefetchCount
        self.Handler = handler

class Consumer(object):
    queue_handlers = None
    connection = None
    stopped_flag = None

    def __init__(self, queue_handlers):
        self.queue_handlers = queue_handlers
        self.stopped_flag = StoppedFlag()

    def on_message(self, queue_name, handler_info, work_queue, channel, method, properties, body):
        message = {}
        message['body'] = body
        message['delivery_tag'] = method.delivery_tag
        work_queue.put(message)

    def on_channel_open(self, queue_name, handler_info, channel):
        work_queue = Queue()
        self.start_worker(channel, self.stopped_flag, work_queue, batch_size=handler_info.PrefetchCount, handler=handler_info.Handler)
        channel.basic_qos(prefetch_count=handler_info.PrefetchCount)
        channel.basic_consume(queue_name, partial(self.on_message, queue_name, handler_info, work_queue))

    def on_connection_open(self, connection):
        for queue_name, handler_info in self.queue_handlers.items():
            connection.channel(on_open_callback=partial(self.on_channel_open, queue_name, handler_info))

    def worker(self,
               channel,
               stopped_flag: StoppedFlag,
               work_queue: Queue,
               batch_size,
               handler):
        while not stopped_flag.is_stopped():
            count = 0
            workload = []
            to_ack = []
            while count < batch_size:
                try:
                    message = work_queue.get(block=True, timeout=5)
                except:
                    break
                workload.append(message['body'].decode())
                to_ack.append(message['delivery_tag'])
                count += 1
            if len(workload) > 0:
                handler(workload)
            if len(to_ack) > 0:
                for delivery_tag in to_ack:
                    channel.basic_ack(delivery_tag=delivery_tag)

    def start_worker(self,
                     channel,
                     stopped_flag: StoppedFlag,
                     work_queue: Queue,
                     batch_size,
                     handler):
        send_thread = threading.Thread(target=self.worker, args=[channel, stopped_flag, work_queue, batch_size, handler])
        send_thread.start()

    def start(self):
        parameters = _get_connection_parameters()
        self.connection = pika.SelectConnection(parameters, on_open_callback=self.on_connection_open)

        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.stopped_flag.stop()
