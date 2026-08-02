"""
=========================================================
Project G-EXO
Logger Module
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import logging
import os
from datetime import datetime

from config import LOG_FILE


os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def log(message, level="INFO"):

    level = level.upper()

    if level == "INFO":
        logging.info(message)

    elif level == "WARNING":
        logging.warning(message)

    elif level == "ERROR":
        logging.error(message)

    elif level == "DEBUG":
        logging.debug(message)

    else:
        logging.info(message)


def log_request(route, message):

    log(
        f"[REQUEST] Route={route} | Message={message}"
    )


def log_response(success, response):

    status = "SUCCESS" if success else "FAILED"

    log(
        f"[RESPONSE] Status={status} | Message={response}"
    )


def log_exception(exception):

    log(
        f"[EXCEPTION] {exception}",
        "ERROR",
    )


def log_separator():

    log("-" * 80)