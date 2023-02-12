from config.config import Config

from service.barcode_processing import BarcodeProcessor
from service.camera_reader import CameraReader



class PipeLine:
    def __init__(self, config: Config = None):
        self.camera_reader = CameraReader(config=config)
        self.barcode_processor = BarcodeProcessor(config=config)
        
    def start(self):
        self.camera_reader.start()
        self.barcode_processor.start()
        
    def join(self):
        self.camera_reader.join()
        self.barcode_processor.join()

    
if __name__ == "__main__":
    pipeline = PipeLine()
    pipeline.start()
    pipeline.join()
        