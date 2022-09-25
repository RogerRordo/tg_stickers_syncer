import logging
import os

from src.runner import Runner
from config import config

if __name__ == '__main__':
    debug_mode = os.environ.get('DEBUG') is not None
    debug_level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(
        level=debug_level,
        format=
        '%(asctime)s %(filename)s[%(lineno)d]: %(levelname)s: %(message)s')

    Runner(config).run()
