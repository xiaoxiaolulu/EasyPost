""" failure type exceptions
    these exceptions will mark test as failure
"""


class BaseError(Exception):

    pass


class SendMessageException(BaseError):

    pass


class MysqlConnectionException(BaseError):

    pass


class MysqlConfigError(BaseError):

    pass


class GetTimestampException(BaseError):

    pass
