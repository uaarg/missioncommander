"""
Configures logging for the application.
"""

import logging 
import logging.handlers
import os

def init(filename="main.log", console_level=logging.CRITICAL, file_level=logging.DEBUG):
    log_dir = os.path.join('data', 'logs')
    log_filename = os.path.join(log_dir, filename)
    os.makedirs(log_dir, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")

    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    rootLogger.addHandler(console_handler)
    rootLogger.addHandler(file_handler)