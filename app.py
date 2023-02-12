import logging

from utils.utils import setup_logging
from pipeline.pipeline import PipeLine
from config.config import Config

setup_logging()


if __name__ == "__main__":
    _config = Config()
    logger = logging.getLogger("MAIN")
    pipeline = PipeLine(config=_config)
    pipeline.start()
    pipeline.join()
