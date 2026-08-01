"""
=========================================================
Project G-EXO
Logger Module
Version : 1.1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

import logging
import os

from config import LOG_FILE


os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def log(message):

    logging.info(message)