import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="sdfsdf  %(asctime)s %(levelname)s [%(name)s] %(message)s"
    )