

class HttpMethodEnum:

    GET_UPPER = "GET"
    GET_LOWER = "get"
    POST_UPPER = "POST"
    POST_LOWER = "post"
    PUT_UPPER = "PUT"
    PUT_LOWER = "put"
    PATCH_UPPER = "PATCH"
    PATCH_LOWER = "patch"
    DELETE_UPPER = "DELETE"
    DELETE_LOWER = "delete"
    HEAD_UPPER = "HEAD"
    HEAD_LOWER = "head"


class ApiHeadersEnum:

    JSON = "application/json"
    FORM_DATA = "multipart/form-data"
    X_WWW_FORM_URLENCODED = "x_www_form_urlencoded"


class ApiModeEnum:

    RAW = "raw"
    FORM_DATA = "formdata"
    X_WWW_FORM_URLENCODED = "x_www_form_urlencoded"
