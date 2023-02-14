import logging
from threading import Thread

import cv2
import numpy as np

from config.config import Config
from common.common import *
from service.buffer_manager import BufferManager


class CameraReader:
    def __init__(self, config: Config = None):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.buffer_manager = BufferManager(config=config)
        self.cap = None
        self.camera_reader = Thread(target=self._camera_reader, daemon=True)

    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.camera_reader.start()

    def join(self):
        self.cap.release()
        self.camera_reader.join()

    def _camera_reader(self):
        try:
            fault_count = 0
            frame_count = 0
            max_retries = 0
            cv2.namedWindow("output", cv2.WINDOW_NORMAL) 
            while self.buffer_manager.event:
                ret, frame = self.cap.read()
                if fault_count >= 200:
                    max_retries += 1
                    if max_retries >= 2:
                        break
                    else:
                        del self.cap
                        self.cap = cv2.VideoCapture(0)
                        fault_count = 0
                if not ret:
                    fault_count += 1
                    continue
                else:
                    frame_count += 1
                    if frame_count >= 5:
                        self.buffer_manager.put_data(queue_name=INPUT_READ_BARCODE, data=frame)
                        frame_count = 0
                cv2.imshow("output", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.buffer_manager.event = False
        except Exception as e:
            self.logger.error(f"Camera reader failed. Error {e}")
    