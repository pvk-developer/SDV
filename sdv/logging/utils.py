"""Utilities for configuring logging within the SDV library."""

import contextlib
import logging
from functools import lru_cache
from pathlib import Path

import platformdirs
import yaml


def get_sdv_logger_config():
    """Return a dictionary with the logging configuration."""
    logging_path = Path(__file__).parent
    with open(logging_path / 'sdv_logger_config.yml', 'r') as f:
        logger_conf = yaml.safe_load(f)

    # Logfile to be in this same directory
    store_path = Path(platformdirs.user_data_dir('sdv', 'sdv-dev'))
    store_path.mkdir(parents=True, exist_ok=True)
    for logger in logger_conf.get('loggers', {}).values():
        handler = logger.get('handlers', {})
        if handler.get('filename') == 'sdv_logs.log':
            handler['filename'] = store_path / handler['filename']

    return logger_conf


@contextlib.contextmanager
def disable_single_table_logger():
    """Temporarily disables logging for the single table synthesizers.

    This context manager temporarily removes all handlers associated with
    the ``SingleTableSynthesizer`` logger, disabling logging for that module
    within the current context. After the context exits, the
    removed handlers are restored to the logger.
    """
    # Logging without ``SingleTableSynthesizer``
    single_table_logger = logging.getLogger('SingleTableSynthesizer')
    handlers = single_table_logger.handlers
    single_table_logger.handlers = []
    try:
        yield
    finally:
        for handler in handlers:
            single_table_logger.addHandler(handler)


@lru_cache()
def get_sdv_logger(logger_name):
    """Get a logger instance with the specified name and configuration.

    This function retrieves or creates a logger instance with the specified name
    and applies configuration settings based on the logger's name and the logging
    configuration.

    Args:
        logger_name (str):
            The name of the logger to retrieve or create.

    Returns:
        logging.Logger:
            A logger instance configured according to the logging configuration
            and the specific settings for the given logger name.
    """
    logger_conf = get_sdv_logger_config()
    if logger_conf.get('log_registry') is None:
        # Return a logger without any extra settings and avoid writing into files or other streams
        return logging.getLogger(logger_name)

    if logger_conf.get('log_registry') == 'local':
        logger = logging.getLogger(logger_name)
        if logger_name in logger_conf.get('loggers'):
            formatter = None
            config = logger_conf.get('loggers').get(logger_name)
            log_level = getattr(logging, config.get('level', 'INFO'))
            if config.get('format'):
                formatter = logging.Formatter(config.get('format'))

            logger.setLevel(log_level)
            logger.propagate = config.get('propagate', False)
            handler = config.get('handlers')
            handlers = handler.get('class')
            handlers = [handlers] if isinstance(handlers, str) else handlers
            for handler_class in handlers:
                if handler_class == 'logging.FileHandler':
                    logfile = handler.get('filename')
                    file_handler = logging.FileHandler(logfile)
                    file_handler.setLevel(log_level)
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
                elif handler_class in ('logging.consoleHandler', 'logging.StreamHandler'):
                    ch = logging.StreamHandler()
                    ch.setLevel(log_level)
                    ch.setFormatter(formatter)
                    logger.addHandler(ch)

        return logger
