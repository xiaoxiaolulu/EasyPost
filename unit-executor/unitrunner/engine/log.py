from unitrunner.engine.env import (
    DEBUG
)


class CaseRunLog:

    def save_log(self, message, level) -> None:
        """
        Saves a log message with a specified level to an internal list.

        This method appends a formatted log message to a list stored as the `log_data` attribute of the object.
        If the `log_data` attribute doesn't exist yet, it creates an empty list first.

        Args:
            message (str): The message to be logged.
            level (str): The level of the message (e.g., "INFO", "WARNING", "ERROR").
        """
        if not hasattr(self, 'log_data'):
            setattr(self, 'log_data', [])
        info = "【{}】 |: {}".format(level, message)
        getattr(self, 'log_data').append(info)

    def save_validators(self, methods, expected, actual, result, state, expect) -> None:
        """
        Saves validation information for later retrieval.

        This method stores information about a validation operation within the object.
        The information includes:

        - `methods`: A list of validation method names used (e.g., ["method1", "method2"]).
        - `expected`: The expected value for the validation.
        - `actual`: The actual value obtained during validation.
        - `result`: The validation result (True for success, False for failure).
        - `state`
        - `expect`

        The information is stored in a list named `validate_extractor` as dictionaries.
        If the `validate_extractor` attribute doesn't exist yet, it's created as an empty list first.

        Args:
            methods (list): A list of validation method names.
            expected (object): The expected value for the validation.
            actual (object): The actual value obtained during validation.
            result (bool): The validation result (True for success, False for failure).
        """
        if not hasattr(self, 'validate_extractor'):
            setattr(self, 'validate_extractor', [])
        info = {"expected": expected, "methods": methods, "actual": actual, "result": result, 'state': state, 'expect': expect}
        getattr(self, 'validate_extractor').append(info)

    def save_extractors(self, name, ext, value) -> None:
        if not hasattr(self, 'data_extractor'):
            setattr(self, 'data_extractor', [])
        info = {"vars_name": name, "type": ext[1], "expression": ext[2], "result": value}
        getattr(self, 'data_extractor').append(info)

    def save_ife(self, info) -> None:
        """
        Saves information for later retrieval with a descriptive name.

        This method stores the provided information (`info`) in a list named `if_extractor`
        associated with the object. If the `if_extractor` attribute doesn't exist yet,
        it's created as an empty list first.

        The purpose of this information and the meaning of "ife" are unclear
        without more context. It might be related to feature extraction or
        interface information, but this is speculation without knowing
        the broader context of the code.

        Args:
            info (object): The information to be saved (type can vary depending on usage).
        """
        if not hasattr(self, 'if_extractor'):
            setattr(self, 'if_extractor', [])
        getattr(self, 'if_extractor').append(info)

    def print(self, *args) -> None:
        """
        Prints a formatted message to an internal log and optionally specifies a log level.

        This method overrides the default built-in `print` function within the class context.
        It takes variable arguments (`*args`) and allows an optional `level` argument to categorize the log message.

        - `args`: Any number of arguments to be included in the log message. These will be converted to strings.
        - `level` (optional, default='INFO'): The log level of the message (e.g., 'INFO', 'WARNING', 'ERROR').

        The formatted message is then appended to the object's internal `log_data` attribute, which is assumed to be
         a list of tuples where the first element represents the log level and the second element is the message itself.

        **Important Note:** This method does not directly print to the console or standard output. It stores the
         message internally for later retrieval or processing using the `log_data` attribute.

        Args:
            *args: Variable positional arguments to be included in the log message.
            level (str, optional): The log level of the message (defaults to 'INFO').
        """
        args = [str(i) for i in args]
        message = ' '.join(args)
        getattr(self, 'log_data').append(('INFO', message))

    def debug_log(self, *args) -> None:
        """
        Logs a debug message if the DEBUG flag is set.

        This method takes variable arguments (`*args`) and constructs a message by joining them together.
        It then checks if a global variable named `DEBUG` is set to `True`. If so, it calls the `save_log`
         method (assumed to exist within the class) to save the message with the level 'DEBUG'.

        **Important Notes:**

        - This method depends on a global variable named `DEBUG` to control whether the message is logged.
          Consider using a class attribute or a configuration setting for better control and maintainability.
        - The `save_log` method is assumed to exist and is responsible for storing the message with the appropriate level.

        Args:
            *args: Variable positional arguments to be included in the debug message.
        """
        if DEBUG:
            message = ''.join(args)
            self.save_log(message, 'DEBUG')

    def info_log(self, *args) -> None:
        """
        Logs an informational message.

        This method takes variable arguments (`*args`) and constructs a message by joining them together.
        It then calls the `save_log` method (assumed to exist within the class) to save the message with
        the level 'INFO'.

        Args:
            *args: Variable positional arguments to be included in the informational message.
        """
        message = ''.join(args)
        self.save_log(message, 'INFO')

    def warning_log(self, *args) -> None:
        """
        Logs a warning message with a warning emoji prepended to each argument.

        This method takes variable arguments (`*args`) and constructs a message by joining
        them together with a warning emoji ('⚠️') in between.
        It then calls the `save_log` method (assumed to exist within the class) to save
        the message with the level 'WARNING'.

        Args:
            *args: Variable positional arguments to be included in the warning message.
        """
        message = '⚠️'.join(args)
        self.save_log(message, 'WARNING')

    def error_log(self, *args) -> None:
        """
        Logs an error message with an error emoji prepended to each argument.

        This method takes variable arguments (`*args`) and constructs a message by
        joining them together with an error emoji ('⛔') in between.
        It then calls the `save_log` method (assumed to exist within the class) to
        save the message with the level 'ERROR'.

        Args:
            *args: Variable positional arguments to be included in the error message.
        """
        message = '⛔'.join(args)
        self.save_log(message, 'ERROR')

    def exception_log(self, *args) -> None:
        """
        Logs an exception message with an error emoji prepended to each argument.

        This method takes variable arguments (`*args`) and constructs a message by joining
        them together with an error emoji ('❌') in between.
        It then calls the `save_log` method (assumed to exist within the class) to save
        the message with the level 'ERROR'.

        Args:
            *args: Variable positional arguments to be included in the exception message.
        """
        message = '❌'.join(args)
        self.save_log(message, 'ERROR')

    def critical_log(self, *args) -> None:
        """
        Logs a critical message with a "U-turn" emoji prepended to each argument.

        This method takes variable arguments (`*args`) and constructs a message by
         joining them together with a "U-turn" emoji ('↪️') in between.
        It then calls the `save_log` method (assumed to exist within the class) to
         save the message with the level 'CRITICAL'.

        **Critical messages** are typically used to indicate severe errors or issues
        that may require immediate attention and potentially halt program execution.

        Args:
            *args: Variable positional arguments to be included in the critical message.
        """
        message = '↪️'.join(args)
        self.save_log(message, 'CRITICAL')
