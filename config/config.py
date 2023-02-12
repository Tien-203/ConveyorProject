import os
import json

from common.common import *
from object.singleton import Singleton


class Config(metaclass=Singleton):
    max_q_size = int(os.getenv(MAX_Q_SIZE, 10))
    log_file = os.getenv(LOG_FILE, "logs/app.log")
    timeout = int(os.getenv(TIMEOUT, 10))

    def __repr__(self):
        return json.dumps({key: getattr(self, key)
                           for key in self.__dir__() if "__" != key[:2] and "__" != key[-2:] and key != "dict"}
                          , indent=4)
