# logging_config.py
import logging
from logging.handlers import TimedRotatingFileHandler

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a rotating log file handler
log_file_handler = TimedRotatingFileHandler('qbitorrent_dl_manager.log', when='midnight', interval=1, backupCount=7)
log_file_handler.setLevel(logging.INFO)
log_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(log_file_handler)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)