import logging.config
from pathlib import Path

logging.config.fileConfig(
    fname=Path('kce_exception_logger.conf'),
    disable_existing_loggers=False,
    defaults={
        'logfilename': 'KCE_logging_file.log'
    },
)

kce_exception_logger = logging.getLogger('kce_exception_logger')
