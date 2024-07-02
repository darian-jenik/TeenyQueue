# config/custom_logger.py

import logging


class CustomLogger(logging.Logger):
    _log_header = '[]'

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def debug(self, msg, *args, **kwargs):
        msg = f'{self._log_header}: {msg}'
        super().warning(msg, *args, **kwargs)

    # Access and other broadcasts.
    def info(self, msg, *args, **kwargs):
        msg = f'{self._log_header}: {msg}'
        super().info(msg, *args, **kwargs)

    # For possible security related events.
    def warning(self, msg, *args, **kwargs):
        msg = f'{self._log_header}: {msg}'
        super().warning(msg, *args, **kwargs)

    # Known unknowns.
    def error(self, msg, *args, **kwargs):
        msg = f'{self._log_header}: {msg}'
        super().error(msg, *args, **kwargs)

    # Stacktrace
    def critical(self, msg, *args, **kwargs):
        msg = f'{self._log_header}: {msg}'
        super().error(msg, *args, **kwargs)


# end
