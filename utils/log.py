import logging
from datetime import datetime
from pathlib import Path
from config.settings import BASE_DIR

log = logging.getLogger(__name__)


def set_log_format(config):
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    config.option.log_file = Path(BASE_DIR).joinpath('logs', f'{current_time}.log')
    config.option.log_file_level = "info"
    config.option.log_file_format = "%(asctime)s [%(levelname)s]: %(message)s"
    config.option.log_file_date_format = "%Y-%m-%d %H:%M:%S"
    config.option.log_cli_level = "info"
    config.option.log_cli_format = '%(asctime)s [%(levelname)s]: %(message)s'
    config.option.log_cli_date_format = '%Y-%m-%d %H:%M:%S'
