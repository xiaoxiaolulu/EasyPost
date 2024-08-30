from typing import Any
import jmespath
import jsonpath
from unitrunner import exceptions


def extract_by_object(response: Any, extract_expression: str) -> Any:
    """
    This function extracts data from the response object based on the provided extraction expression.

    Parameters:
    response (Any): The response object from which data is to be extracted.
    extract_expression (str): The extraction expression used to extract data from the response.

    Returns:
    Any: The extracted data.
    """

    if extract_expression.startswith("$."):
        try:
            extract_value = jsonpath.jsonpath(response, extract_expression)
            return extract_value
        except exceptions.ExtractException as err:
            raise PermissionError(f'❌expression:<{extract_expression}>, error: {err}')
    else:
        try:
            extract_value = jmespath.search(response, extract_expression)
            return extract_value
        except exceptions.ExtractException as err:
            raise PermissionError(f'❌expression:<{extract_expression}>, error: {err}')
