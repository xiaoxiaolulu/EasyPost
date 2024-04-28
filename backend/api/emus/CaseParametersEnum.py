from enum import IntEnum


class CaseParametersEnum(IntEnum):

    NONE = 0
    RAW = 1
    HEADER = 2
    FORM_DATA = 3
    X_WWW_FORM_URLENCODED = 4
