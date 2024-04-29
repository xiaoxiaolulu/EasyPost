import inspect
import io
import os
import sys
from loguru import logger as uru_logger
from config import settings


class Log:

    logger = uru_logger

    def __init__(self, name='EasyPost', level='DEBUG'):
        self.business = name
        self._configure_handlers(level)

    def _configure_handlers(self, level):
        base_log_dir = settings.BASE_LOG_DIR
        os.makedirs(base_log_dir, exist_ok=True)

        self.logger.remove()  # 移除默认的 StreamHandler
        self.logger.add(
            sys.stdout,
            level=level.upper(),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
                   "<m>[{thread.name}]</m>-"
                   "<cyan>[{module}</cyan>.<cyan>{function}</cyan>"
                   ":<cyan>{line}]</cyan>-"
                   "<blue>[{level}]</blue>: "
                   "<magenta>{message}</magenta>"
        )
        self.logger.add(
            os.path.join(base_log_dir, f"{self.business}.log"),
            level=level.upper(),
            format="{time:YYYY-MM-DD HH:mm:ss} "
                   "[{thread.name}]-"
                   "[{module}.{function}:{line}]-[{level}]:{message}",
            rotation="10 MB",
            encoding="utf-8"
        )

    @classmethod
    def change_level(cls, level):

        cls.logger.remove(0)  # 移除控制台 handler
        cls.logger.add(
            sys.stdout,
            level=level.upper(),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
                   "<m>[{process.name}]</m>-"
                   "<m>[{thread.name}]</m>-"
                   "<cyan>[{module}</cyan>.<cyan>{function}</cyan>"
                   ":<cyan>{line}]</cyan>-"
                   "<level>[{level}]</level>: "
                   "<level>{message}</level>"
        )

    def log(self, level, message):
        frame = inspect.currentframe().f_back
        func, line, filename = inspect.getframeinfo(frame).function, frame.f_lineno, frame.f_code.co_filename
        self.logger.bind(name=getattr(settings, f"EASY_POST_{level.upper()}", level),
                         func=func, line=line, business=self.business, filename=filename).log(level, message)

    def debug(self, message):
        self.log("DEBUG", message)

    def info(self, message):
        self.log("INFO", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)

    def exception(self, message):
        self.log("EXCEPTION", message)

    @staticmethod
    def print(message):
        sys.stdout.write("<green>{time:YYYY-MM-DD HH:mm:ss}</green> ")


_logger = Log()
logger = _logger.logger
