import logging
from queue import Queue

from config.config import Config
from object.singleton import Singleton


class BufferManager(metaclass=Singleton):

    def __init__(self, config: Config = None):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = Config()
        self.list_queue = {}
        self.event = True

    def add_queue(self, queue_name: str):
        if queue_name not in self.list_queue:
            self.list_queue[queue_name] = Queue(maxsize=self.config.max_q_size)
            self.logger.info(f"Successfully create Queue {queue_name}")
        else:
            self.logger.info(f"{queue_name} already exists in list queue")

    def get_data(self, queue_name: str, timeout: int = None):
        try:
            if queue_name in self.list_queue:
                if timeout:
                    output = self.list_queue[queue_name].get(timeout=timeout)
                else:
                    output = self.list_queue[queue_name].get()
                # self.logger.info(f"GET ITEM FROM {queue_name}. {self.list_queue[queue_name].qsize()} ITEMS REMAINS")
                return output
            else:
                self.add_queue(queue_name=queue_name)
                if timeout:
                    output = self.list_queue[queue_name].get(timeout=timeout)
                else:
                    output = self.list_queue[queue_name].get()
                # self.logger.info(f"GET ITEM FROM {queue_name}. {self.list_queue[queue_name].qsize()} ITEMS REMAINS")
                return output
        except Exception as e:
            self.logger.info(f"Get data time out: {e}")

    def put_data(self, queue_name: str, data):
        if queue_name in self.list_queue:
            self.list_queue[queue_name].put(data)
            # self.logger.info(f"PUT ITEM TO {queue_name}. {self.list_queue[queue_name].qsize()} ITEMS REMAINS")
        else:
            self.add_queue(queue_name=queue_name)
            self.list_queue[queue_name].put(data)
            # self.logger.info(f"PUT ITEM TO {queue_name}. {self.list_queue[queue_name].qsize()} ITEMS REMAINS")
