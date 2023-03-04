import logging

logging.basicConfig(format='[%(levelname)s] [%(asctime)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def info(message) -> None:
    logging.info(message)

def warning(message) -> None:
    logging.warning(message)

def error(message) -> None:
    logging.error(message)