from queue import Queue
from threading import Thread
import warnings
import logging

import numpy as np
from pyzbar.pyzbar import decode
import cv2

from service.buffer_manager import BufferManager
from object.frame import Frame
from config.config import Config
from common.common import *

warnings.filterwarnings("ignore")


class BarcodeProcessor:
    def __init__(self, config: Config = None):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.buffer_manager = BufferManager(config=config)
        self.barcode_reader = Thread(target=self._barcode_reader, daemon=True)
        self.data_retriver = Thread(target=self._data_retriver, daemon=True)

    def start(self):
        self.barcode_reader.start()
        self.data_retriver.start()

    def join(self):
        self.barcode_reader.join()
        self.data_retriver.join()

    def _barcode_reader(self):
        while self.buffer_manager.event:
            print(11111, self.buffer_manager.event)
            try:
                image: np.ndarray = self.buffer_manager.get_data(queue_name=INPUT_READ_BARCODE, timeout=self.config.timeout)
                if image is None:
                    continue
                detectedBarcodes = decode(image)
                list_barcode = []
                if detectedBarcodes:
                    for barcode in detectedBarcodes: 
                        # cv2.rectangle(image, (x-10, y-10),
                        #             (x + w+10, y + h+10),
                        #             (255, 0, 0), 2)
                        # if barcode.data!="":
                        #     image = cv2.putText(image, f"{barcode.data}", (x-12, y-12), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                        #     print(barcode.data)
                        if barcode.data:
                            (x, y, w, h) = barcode.rect
                            list_barcode.append([[x - 10, y - 10, x + w + 10, y + h +10], barcode.data])
                            self.logger.info(f"Detected barcode. {barcode.data}")
                if list_barcode:
                    self.buffer_manager.put_data(queue_name=OUTPUT_READ_BARCODE, data=Frame(image=image, barcode=list_barcode, config=self.config))
            except Exception as e:
                self.logger.error(f"Barcode reader failed. Error: {e}")

    def _data_retriver(self):
        try:
            while self.buffer_manager.event:
                frame: Frame = self.buffer_manager.get_data(queue_name=OUTPUT_READ_BARCODE, timeout=self.config.timeout)
                # TODO connect to database
        except Exception as e:
            self.logger.error(f"Data retriver failed. Error: {e}")
