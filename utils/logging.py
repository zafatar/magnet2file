import os
import logging

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s [%(process)s] %(name)s:%(lineno)d – %(message)s',
)


def get_logger(debug: bool=False) -> logging.Logger:
    # Prepare and set the logger
    logger = logging.getLogger()

    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("****************************")
        logger.debug("*** Debug mode is active ***")
        logger.debug("****************************")
    else:
        logger.setLevel(logging.INFO)

    return logger

logger = get_logger(os.getenv('DEBUG', True))
