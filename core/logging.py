import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
from .app_config import config

def setup_logger() -> None:
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

    # 오늘 날짜 기반 파일명 생성
    log_dir = config.LOG_DIR
    log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(log_dir, log_filename)

    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        log_path,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=log_level,
        handlers=[console_handler, file_handler]
    )

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
