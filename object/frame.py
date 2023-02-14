from typing import List

import numpy as np

from config.config import Config
from common.common import *


class Frame:
    def __init__(self,  image: np.ndarray, barcode: List, config: Config = None):
        self.config = config
        self.image = image
        self.barcode = barcode
        self.data_from_server = None

    @classmethod
    def new_frame(cls, image: np.ndarray, barcode: List = None):
        return cls(image=image, barcode=barcode, config=cls.config)

    @property
    def info(self):
        return {
            IMAGE: self.image,
            BARCODE: self.barcode[1],
            DATA: self.data_from_server
        }
