import os
from logging import getLogger
from logging.config import dictConfig

from settings import LOG_DIR, LOGGING


def configure_logger():
    logger = getLogger(__name__)

    try:
        os.mkdir(LOG_DIR)
    except OSError as e:
        if e.errno == 17:
            pass
        else:
            logger.exception('%s %s', e.strerror, e.filename)

    dictConfig(LOGGING)

    return logger
