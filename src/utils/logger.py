import logging


def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger("MyLogger")
    logger.setLevel(
        logging.DEBUG
    )  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    # Create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)

    return logger
