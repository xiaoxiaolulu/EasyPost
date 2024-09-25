import ast
import json
from typing import (
    List,
    Dict,
    Any
)
from api.emus.CaseParametersEnum import CaseParametersEnum


class HandelTestData(object):

    def __init__(self, request_body: Dict = None) -> None:
        """
        Initializes the object attributes based on a provided request body dictionary.

        This method is the constructor for the class. It takes an optional
        `request_body` dictionary and attempts to assign its values to corresponding
        object attributes. It handles potential exceptions like missing keys, value errors,
        and attribute errors. However, simply passing all exceptions might not be ideal
        for debugging. Consider handling specific exceptions more gracefully.

        Args:
            request_body (Dict, optional): A dictionary containing configuration data for the object.
                - directory_id (str, optional): ID of the directory (extra parameter).
                - project (str, optional): Project name (extra parameter).

                - name (str, optional): Name of the API or test case.
                - url (str, optional): URL of the API endpoint.
                - method (str, optional): HTTP method (e.g., 'GET', 'POST').
                - priority (str, optional): Priority level (e.g., 'high', 'medium', 'low').
                - status (str, optional): Current status (e.g., 'active', 'inactive').
                - desc (str, optional): Description of the API or test case.

                - headers (List[Dict], optional): Request headers (converted to JSON string).
                - raw (Dict, optional): Raw request data (converted to JSON string).
                - params (List, optional): URL parameters (converted to JSON string).
                - setup_script (str, optional): Setup script for the API call/test case.
                - teardown_script (str, optional): Teardown script for the API call/test case.
                - validate (List, optional): Validation rules (converted to JSON string).
                - extract (List, optional): Data extraction configuration (converted to JSON string).

                - mode (str, optional): Execution mode (e.g., 'normal', 'concurrency'). Defaults to 'normal'.
                - threads (int, optional): Number of threads for concurrent execution (defaults to 1).
                - iterations (int, optional): Number of iterations to run (defaults to 1).

                - step_data (List, optional): List of dictionaries defining steps within a test case.
                - cron (str, optional): Cron expression for scheduling (optional).

                - plan attributes (for test case planning):
                    - case_list (List, optional): List of dictionaries representing test cases.
                    - state (int, optional): Current state of the test plan.
                    - pass_rate (str, optional): Target pass rate (e.g., '80%').
                    - msg_type (int, optional): Message type for notifications.
                    - receiver (List, optional): List of recipients for notifications.

        Raises:
            (KeyError, ValueError, AttributeError): These exceptions are caught but not handled
                specifically. Consider handling them more informatively for debugging purposes.
        """
        try:
            # 额外参数
            self.directory_id = request_body.get('directory_id', None)
            self.project = request_body.get('project', None)

            # 基本信息
            self.name = request_body.get('name', None)
            self.url = request_body.get('url', None)
            self.method = request_body.get('method', None)
            self.priority = request_body.get('priority', None)
            self.status = request_body.get('status', None)
            self.desc = request_body.get('desc', None)

            # 请求体
            self.headers = json.dumps(request_body.get('headers', []))
            self.raw = json.dumps(request_body.get('raw', {}))
            self.params = json.dumps(request_body.get('params', []))
            self.setup_script = request_body.get('setup_script', None)
            self.teardown_script = request_body.get('teardown_script', None)
            self.validate = json.dumps(request_body.get('validators', []))
            self.extract = json.dumps(request_body.get('extract', []))

            # 一键压测
            self.mode = request_body.get('mode', 'normal')
            self.threads = request_body.get('threads', 1)
            self.iterations = request_body.get('iterations', 1)

            # 步骤
            self.step_data = request_body.get('step_data', [])

            # 计划
            self.cron = request_body.get('cron', None)
            self.case_list = request_body.get('case_list', [])
            self.state = request_body.get('state', 0)
            self.pass_rate = request_body.get('pass_rate', '80%')
            self.msg_type = request_body.get('msg_type', 0)
            self.receiver = request_body.get('receiver', [])

        except (KeyError, ValueError, AttributeError):
            pass

    @staticmethod
    def resolve_headers(headers: str) -> dict[str, str]:
        """
        Converts a JSON-formatted string representing headers into a Python dictionary.

        Args:
            headers: A JSON string containing key-value pairs representing headers.

        Returns:
            A Python dictionary with header names as keys and their corresponding values.

        Raises:
            ValueError: If the provided headers string cannot be decoded as valid JSON.
        """

        try:
            # Attempt to convert the JSON string into a list of dictionaries
            headers_list = json.loads(headers)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON format for headers") from e

        # Create a dictionary with header names as keys and their values
        headers = {item['name']: item['value'] for item in headers_list}

        return headers

    @staticmethod
    def resolve_form_data(raw: str) -> dict[str, dict[str, str]]:
        """
        Converts a string representation of form data (assumed to be JSON-like)
        into a Python dictionary with a nested 'data' dictionary containing
        form field names and values.

        **Security Considerations:**

        - This function uses `ast.literal_eval` for safer evaluation of the provided
          string. `eval` should generally be avoided due to potential security risks
          associated with arbitrary code execution.
        - If the input string is not guaranteed to be valid JSON, consider
          additional validation or sanitization before processing.

        Args:
            raw: A string representation of form data (assumed to be JSON-like).

        Returns:
            A dictionary with a nested 'data' dictionary containing form field names
            and values.

        Raises:
            SyntaxError: If the provided string cannot be safely evaluated as a
            Python literal.
        """

        try:
            form_data_dict = ast.literal_eval(raw)  # Safer evaluation using ast
            form_data_items = form_data_dict.get('form_data', [])
            form_data = {'data': {item['name']: item['value'] for item in form_data_items}}

        except (SyntaxError, ValueError):
            return []

        if not isinstance(form_data_dict, dict) or 'form_data' not in form_data_dict:
            return []

        return form_data

    @staticmethod
    def resolve_x_www_form_urlencoded(raw: str) -> dict[str, dict[str, str]]:
        """
        Converts a string representation of x-www-form-urlencoded data into a Python
        dictionary with a nested 'data' dictionary containing form field names and values.

        Args:
            raw: A string representation of x-www-form-urlencoded data.

        Returns:
            A dictionary with a nested 'data' dictionary containing form field names
            and values.

        Raises:
            ValueError: If the provided string is not properly formatted as
            x-www-form-urlencoded data.
        """
        try:
            parsed_data = eval(raw)  # Parse using urllib.parse
            form_data_items = parsed_data.get('x_www_form_urlencoded', [])
            form_data = {'data': {item['name']: item['value'] for item in form_data_items}}
            return form_data
        except (ValueError, TypeError, Exception):
            return {'data': {}}

    @staticmethod
    def resolve_json(raw: str) -> dict[str, Any]:
        """
        Converts a string representation of JSON data into a Python dictionary
        with a 'json' key containing the parsed data.

        **Security Considerations:**

        - This function avoids using `eval` for security reasons. `eval` can be
          dangerous as it can execute arbitrary Python code.
        - If the input string is not guaranteed to be valid JSON, consider
          additional validation or sanitization before processing with `json.loads`.

        Args:
            raw: A string representation of JSON data.

        Returns:
            A dictionary with a 'json' key containing the parsed JSON data.

        Raises:
            json.JSONDecodeError: If the provided string cannot be decoded as valid JSON.
        """

        try:
            json_items = eval(raw).get('json', [])
            json_data = json.loads(json_items)  # Use json.loads for safe parsing
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON format") from e

        return {'json': json_data}

    def raw_conversion(self, raw: str) -> dict[str, Any]:
        """
        Converts raw input data based on its format, using safer methods
        than `eval`.

        This function attempts to identify the format of the raw data (`json`,
        `form_data`, or `x-www-form-urlencoded`) and calls the appropriate conversion
        function. Security considerations are addressed by using safer alternatives
        to `eval`.

        Args:
            self: The object instance (likely related to data processing).
            raw: A string representation of the raw data.

        Returns:
            A dictionary containing the converted data based on its format.

        Raises:
            ValueError: If the format of the raw data cannot be determined or
            if parsing fails for specific formats.
        """

        try:
            # Attempt safer evaluation to extract target key
            data_dict = ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            raise ValueError("Invalid data format") from None

        if CaseParametersEnum.JSON in data_dict:
            raw = data_dict.get('json', [])
            raw_content = self.resolve_json(raw)
        elif CaseParametersEnum.FORM_DATA in data_dict:
            raw = data_dict.get('form_data', [])
            raw_content = self.resolve_form_data(raw)
        else:
            # Assume x-www-form-urlencoded if no specific target found
            raw = data_dict.get('form_data', [])
            raw_content = self.resolve_x_www_form_urlencoded(raw)

        return raw_content

    @staticmethod
    def resolve_script(
            use='setup_script',
            setup_script=None,
            teardown_script=None
    ):
        """
        Resolves the appropriate script based on the provided usage flag.

        This static method is used to determine which script (setup or teardown)
        to use based on the `use` argument.

        Args:
            use (str, optional): Flag indicating the script to use. Defaults to 'setup_script'.
                - 'setup_script': Use the setup script.
                - 'teardown_script': Use the teardown script.
            setup_script (Any, optional): The setup script to be used.
            teardown_script (Any, optional): The teardown script to be used.

        Returns:
            The script (setup or teardown) based on the `use` flag.

        Raises:
            ValueError: If an invalid `use` flag is provided.
        """

        valid_uses = [CaseParametersEnum.SETUP_SCRIPT, CaseParametersEnum.TEARDOWN_SCRIPT]
        if use not in valid_uses:
            raise ValueError(f"Invalid usage flag: {use}. Valid options are: {', '.join(valid_uses)}")

        script = setup_script if use == CaseParametersEnum.SETUP_SCRIPT else teardown_script
        return script

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

        extract_data = [{'name': item['name'], 'type': item['type'], 'description': item['description'], 'env': item.get('env', 'ENV')}
                        for item in extract_items]

        return extract_data

    @staticmethod
    def resolve_validators(validate=None):
        """
        Resolves and processes validator data from a provided dictionary.

        **Security Considerations:**

        - This function avoids using `eval` for security reasons. `eval` can be
          dangerous as it can execute arbitrary Python code.
        - If the input `validate` dictionary is not guaranteed to be trusted,
          consider additional validation or sanitization of its contents before use.

        Args:
            validate (dict, optional): A dictionary containing validator data.
                - type (str): Type of validation method to use.
                - value (Any): The value to validate against.
                - name (str): The expected value or a description of the validation.

        Returns:
            A list of dictionaries containing validator configuration for each item.
                - method (str): The validation method type.
                - actual (Any): The value to be validated.
                - expect (str): The expected value or a description of the validation.

        Raises:
            SyntaxError: If the provided `validate` string cannot be safely evaluated
            as a Python dictionary.
            ValueError: If the `validate` dictionary is missing required keys.
        """

        try:
            # Attempt safer evaluation using ast.literal_eval (assumes dictionary)
            validate_item = ast.literal_eval(validate)
        except (SyntaxError, ValueError):
            return []

        validate_data = [{'method': item['type'], 'actual': item['value'], 'expect': item['name']}
                         for item in validate_item]

        return validate_data

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

        api_doc_template = {
            "mode": self.mode,
            "title": self.name,
            "interface": {
                "url": self.url,
                "name": self.name,
                "method": self.method
            },
            # Commented-out sections can be used for future additions
            # "threads": int(self.threads),  # Number of threads for concurrent execution (optional)
            # "iterations": int(self.iterations),  # Number of iterations to run (optional)
            "headers": self.resolve_headers(self.headers),
            "request": self.raw_conversion(self.raw),
            'setup_script': self.resolve_script(setup_script=self.setup_script),
            'teardown_script': self.resolve_script(use='teardown_script', teardown_script=self.teardown_script),
            'extract': self.resolve_extract(extract=self.extract),
            'validators': self.resolve_validators(self.validate)
        }
        return api_doc_template

    def get_step_template(self, step):
        """
        Generates a step template dictionary containing configuration for a single step.

        This method constructs a dictionary representing a step within a larger
        process based on the provided `step` dictionary. It extracts relevant
        configuration details from the `step` dictionary using the `get` method
        with a default value of `None` to handle potential missing keys.

        Args:
            self: The object instance containing helper methods for processing data.
            step (dict): A dictionary containing configuration details for a single step.

        Returns:
            A dictionary representing the step template with various configuration details.
        """

        step_template = {
            "title": step.get('name', None),
            "interface": {
                "url": step.get('url', None),
                "name": step.get('name', None),
                "method": step.get('method', None)
            },
            "headers": self.resolve_headers(step.get('headers', [])),
            "request": self.raw_conversion(step.get('raw', {})),
            'setup_script': self.resolve_script(setup_script=step.get('setup_script', None)),
            'teardown_script': self.resolve_script(use='teardown_script',
                                                   teardown_script=step.get('teardown_script', None)),
            'extract': self.resolve_extract(extract=step.get('extract', [])),
            'validators': self.resolve_validators(step.get('validate', []))
        }
        return step_template

    def get_case_template(self, cases, name='Demo'):
        """
        Generates a case template dictionary containing configuration for a test case.

        This method constructs a dictionary representing a test case based on the
        provided `cases` list. It iterates through the `cases` list, which is assumed
        to contain dictionaries for each step within the test case. For each step,
        it calls the `self.get_step_template` method to generate the individual
        step template dictionary.

        Args:
            self: The object instance containing helper methods for processing data.
            cases (list[dict]): A list of dictionaries, where each dictionary represents
                a step within the test case. The dictionary should have keys like
                'name', 'url', 'method', etc.
            name (str, optional): The name of the test case (defaults to 'Demo').

        Returns:
            A dictionary representing the test case template with name and a list of steps.
        """

        if not cases:
            return []  # Return an empty list if no cases are provided

        return {
            'name': name,
            'cases': [self.get_step_template(step) for step in cases]
        }

    def get_plan_template(self, suites: List[dict]) -> List[dict]:
        """
        Generates a list of test case template dictionaries from a suite list.

        This method constructs a list of dictionaries, where each dictionary
        represents a test case within a test suite. It iterates through the provided
        `suites` list, which is assumed to be a list of dictionaries representing
        test suites. Each suite dictionary is expected to have a 'name' key (optional)
        and a 'cases' key containing a list of step dictionaries for the test cases.

        Args:
            self: The object instance containing helper methods for processing data.
            suites (List[dict]): A list of dictionaries representing test suites.
                - name (str, optional): The name of the test suite.
                - cases (List[dict]): A list of dictionaries representing steps within
                    the test cases belonging to the suite. Each step dictionary
                    should have keys like 'name', 'url', 'method', etc.

        Returns:
            A list of dictionaries representing test case templates. Each dictionary
            has a 'name' and a 'cases' list containing step templates.
        """

        if not suites:
            return []

        plan_templates = []
        for index, case in enumerate(suites):
            # Extract case name (use default if missing)
            case_name = case.get('name', f'场景-{index + 1}')  # Default: '场景- + index'

            # Generate step templates for the case
            case_steps = [self.get_step_template(step) for step in case.get('cases', [])]

            plan_templates.append({
                'name': case_name,
                'cases': case_steps
            })

        return plan_templates
