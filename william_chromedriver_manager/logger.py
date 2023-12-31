import logging
import os

loggers = {}


def log(text, level=logging.INFO, name="CDM", first_line=False, formatter='[%(name)s] - %(message)s'):
    log_level = os.getenv('CDM_LOG_LEVEL')
    if log_level:
        level = int(log_level)
    if loggers.get(name):
        loggers.get(name).info(text)
    else:
        _logger = logging.getLogger(name)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(formatter)
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        _logger.setLevel(level)
        loggers[name] = _logger
        _logger.info(text)
