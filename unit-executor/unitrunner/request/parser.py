import ast
import json
from typing import (
    Dict
)


class HandelTestData(object):

    def __init__(self, request_body: Dict = None) -> None:
        try:
            self.extract = json.dumps(request_body.get('extract', []))
            self.request_body = request_body

        except (KeyError, ValueError, AttributeError):
            pass

    @staticmethod
    def resolve_extract(env="env", extract=None):
        """
        Resolves and processes extraction data based on a provided dictionary.

        **Security Considerations:**

        - This function avoids using `eval` for security reasons. `eval` can be
          dangerous as it can execute arbitrary Python code.
        - If the input `extract` dictionary is not guaranteed to be trusted,
          consider additional validation or sanitization of its contents before use.

        Args:
            env (str, optional): The environment to use (defaults to "env").
            extract (dict, optional): A dictionary containing extraction data.
                - name (str): Name of the item to extract.
                - type (str): Type of the extracted value.
                - value (Any): The value to extract or a path to extract from the environment.

        Returns:
            A dictionary with extracted items as keys and tuples containing
            (environment, type, value) for each item.

        Raises:
            SyntaxError: If the provided `extract` string cannot be safely evaluated
            as a Python dictionary.
            ValueError: If the `extract` dictionary is missing required keys.
        """

        try:
            # Attempt safer evaluation using ast.literal_eval (assumes dictionary)
            extract_items = ast.literal_eval(extract)
        except (SyntaxError, ValueError):
            return []

        extract_data = {item['name']: (env, item['type'], item['description']) for item in extract_items}
        return extract_data

    def get_api_template(self):
        """
        Generates an API template dictionary containing configuration for an API call.

        This method constructs a dictionary representing an API call based on the
        object's attributes (self.*). These attributes are expected to be set
        appropriately before calling this method.

        Args:
            self: The object instance containing attributes for API configuration.

        Returns:
            A dictionary representing the API template with various configuration details.
        """
        api_doc_template = self.request_body
        api_doc_template = {**api_doc_template, **{'extract': self.resolve_extract(extract=self.extract)}}
        return api_doc_template
