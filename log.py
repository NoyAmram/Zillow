import logging
import zillow_config as cfg


def setup_custom_logger(__name__):
    """ create global logger to be used from different python files.
    Logger information is saved in file under the project directory."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create Formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - FILE:%(filename)s - FUNC:%(funcName)s - LINE:%(lineno)d - %(message)s')

    # create a file handler and add it to logger
    file_handler = logging.FileHandler(cfg.LOG_FILE)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
