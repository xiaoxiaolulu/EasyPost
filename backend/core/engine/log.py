from core.engine.env import (
    DEBUG
)


class CaseRunLog:

    def save_log(self, message, level) -> None:
        if not hasattr(self, 'log_data'):
            setattr(self, 'log_data', [])
        info = "【{}】 |: {}".format(level, message)
        getattr(self, 'log_data').append(info)

    def save_validators(self, methods, expected, actual, result) -> None:
        if not hasattr(self, 'validate_extractor'):
            setattr(self, 'validate_extractor', [])
        info = {"expected": expected, "methods": methods, "actual": actual, "result": result}
        getattr(self, 'validate_extractor').append(info)

    def save_ife(self, info) -> None:
        if not hasattr(self, 'if_extractor'):
            setattr(self, 'if_extractor', [])
        getattr(self, 'if_extractor').append(info)

    def print(self, *args) -> None:
        args = [str(i) for i in args]
        message = ' '.join(args)
        getattr(self, 'log_data').append(('INFO', message))

    def debug_log(self, *args) -> None:
        if DEBUG:
            message = ''.join(args)
            self.save_log(message, 'DEBUG')

    def info_log(self, *args) -> None:
        message = ''.join(args)
        self.save_log(message, 'INFO')

    def warning_log(self, *args) -> None:
        message = '⚠️'.join(args)
        self.save_log(message, 'WARNING')

    def error_log(self, *args) -> None:
        message = '⛔'.join(args)
        self.save_log(message, 'ERROR')

    def exception_log(self, *args) -> None:
        message = '❌'.join(args)
        self.save_log(message, 'ERROR')

    def critical_log(self, *args) -> None:
        message = '↪️'.join(args)
        self.save_log(message, 'CRITICAL')
