import logging.config
from pathlib import Path

try:
    logging.config.fileConfig(
        fname=Path('kce_exception_logger.conf'),
        disable_existing_loggers=False,
        defaults={
            'logfilename': 'KCE_logging_file.log'
        },
    )

    kce_exception_logger = logging.getLogger('kce_exception_logger')
except Exception as e:
    print(e)
    print('Unable to setup KCE logger, config file is most likely missing. Setting up Console logger.')

    kce_exception_logger = logging.getLogger('kce_exception_logger')
