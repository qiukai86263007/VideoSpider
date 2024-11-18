# log_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

# 当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 设置日志记录
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = RotatingFileHandler(
    os.path.join(current_dir, '..', 'logs', 'download_log.log'),
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5  # Keep up to 5 backup files
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)