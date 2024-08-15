""" failure type exceptions
    these exceptions will mark test as failure
"""


class BaseError(Exception):

    pass


class GetRequestException(BaseError):

    pass


class SendRequestException(BaseError):

    pass


class SendMessageException(BaseError):

    pass


class MysqlConnectionException(BaseError):

    pass


class MysqlConfigError(BaseError):

    pass


class VariableReferencesException(BaseError):

    pass


class AssertException(BaseError):

    pass


class AssertFailException(BaseError):

    pass


class RequestPreconditionException(BaseError):

    pass


class ResponsePostConditionException(BaseError):

    pass


class StepMissAttributeError(BaseError):

    pass


class EngineConfigException(BaseError):

    pass


class ApiEndpointsEmptyException(BaseError):

    pass


class BomberRunnerException(BaseError):

    pass


class ExtractException(BaseError):

    pass


class GetTimestampException(BaseError):

    pass


class StepRuntimeError(BaseError):

    pass
