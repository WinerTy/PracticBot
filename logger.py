import logging
from logging.handlers import RotatingFileHandler
import os


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logger = logging.getLogger(__name__)


logger.setLevel(logging.DEBUG)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)


file_handler = RotatingFileHandler(
    filename=os.path.join(log_dir, "bot.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))


logger.addHandler(file_handler)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(console_handler)
