import atomic_bomb_engine
from typing import (
    Dict,
    List,
    Any
)
from api.emus.CaseParametersEnum import CaseParametersEnum


class AtomicBombEngine:

    def __init__(
            self,
            test_duration_secs=None,
            concurrent_requests=None,
            timeout_secs=0,
            cookie_store_enable=True,
            verbose=False,
            increase_step=None,
            increase_interval=None,
            weight=100
    ):
        """
        Initialize the AtomicBombEngine with configuration options.

        Keyword Arguments:
            test_duration_secs (int, optional): Duration of the test in seconds.
            concurrent_requests (int, optional): Number of concurrent requests.
            timeout_secs (int): Request timeout in seconds (default 0).
            cookie_store_enable (bool, optional): Enable cookie storage (default True).
            verbose (bool, optional): Enable verbose logging (default False).
            increase_step (int, optional): Step size for increasing load (default None).
            increase_interval (int, optional): Interval between load increases (default None).
            weight (int, optional): Weight for the test (default 100).
        """

        self.weight = weight
        self.verbose = verbose
        self.cookie_store_enable = cookie_store_enable
        self.timeout_secs = timeout_secs
        self.increase_interval = increase_interval
        self.increase_step = increase_step
        self.concurrent_requests = concurrent_requests
        self.test_duration_secs = test_duration_secs
        self.increase_step = increase_step
        self.increase_interval = increase_interval

    def step_option(self) -> Dict[str, int] | None:
        """
        Create a step option dictionary for the BatchRunner if both increase parameters are provided.
        """
        if self.increase_step is not None and self.increase_interval is not None:
            return atomic_bomb_engine.step_option(self.increase_step, self.increase_interval)
        else:
            return None

    def create_engine_config(self) -> dict:
        """
        Creates a dictionary containing configuration parameters for the engine.

        This function gathers various settings from the class instance and combines
        them into a dictionary that can be easily passed to the `engine.run` method.

        Returns:
            dict: A dictionary containing engine configuration options.
        """
        try:
            engine_config = {
                "test_duration_secs": self.test_duration_secs,
                "concurrent_requests": self.concurrent_requests,
                "step_option": self.step_option(),
                "timeout_secs": self.timeout_secs,
                "cookie_store_enable": self.cookie_store_enable,
                "verbose": self.verbose,
            }
            return engine_config
        except (Exception, ):
            raise AttributeError("Could not create engine configuration")

    def run(self, data: Dict[str, Any]):
        """
        Run the test using the BatchRunner with provided data and engine configuration.

        Args:
            data (Dict[str, Any]): Dictionary containing test data.

        Returns:
            BatchRunner: The initialized BatchRunner object.
        """

        config = self.create_engine_config()
        data = self.raw_conversion(data)
        config["api_endpoints"] = self.step(data)
        runner = atomic_bomb_engine.BatchRunner()
        runner.run(**config)
        return runner

    def step(self, data: Dict[str, Any]) -> List[List[Any]]:
        """
        Create a list of API endpoint lists based on the provided data.

        Args:
            data (Dict[str, Any]): Dictionary containing test data.

        Returns:
            List[List[Any]]: A list containing a single list of API endpoint details.
        """

        api_endpoints = []
        try:
            endpoint = getattr(atomic_bomb_engine, 'endpoint')
            assert_options = self.assert_option(data.get("validators"))
            del data["validators"]
            api_endpoints.append(endpoint(
                **data,
                weight=self.weight,
                assert_options=assert_options
            ))
            return api_endpoints

        except (AttributeError, TypeError, ValueError):
            return api_endpoints

    @staticmethod
    def raw_conversion(raw: dict) -> dict[str, Any]:
        """
        Converts a raw dictionary to a dictionary representing data format and content.

        Args:
            raw (dict): The raw dictionary containing data.

        Returns:
            dict[str, Any]: A dictionary with keys like "json" or "form_data"
                             holding the corresponding data from the raw dictionary,
                             or raises a ValueError if the format is invalid.

        Raises:
            ValueError: If the data format is invalid or the raw dictionary cannot be parsed.
        """
        supported_formats = {CaseParametersEnum.JSON, CaseParametersEnum.FORM_DATA}
        format_key = next((key for key in raw if key in supported_formats), None)

        if format_key:
            return {format_key: raw.get(format_key, None), **raw}
        else:
            return raw

    @staticmethod
    def assert_option(validate_check: list) -> List[Any]:
        """
        Process validation checks from data and potentially call a separate assert function.

        Args:
            validate_check (list): List of validation check dictionaries.

        Returns:
            List[Any]: Potentially a list of processed assert options (implementation might vary).
        """

        assert_options = []
        # Assuming assert_item is a separate function for validation logic (not shown)
        for check in validate_check:
            jsonpath = check.get('jsonpath', None)
            reference_object = check.get('reference_object', None)
            # Placeholder for potential assert_item call with validation logic
            # assert_item(methods=methods, reference_object=expect)
            assert_options.append(atomic_bomb_engine.assert_option(jsonpath, reference_object))

        return assert_options


async def performance(
        test_data,
        test_duration_secs=None,
        concurrent_requests=None,
        timeout_secs=0,
        cookie_store_enable=True,
        verbose=False,
        increase_step=None,
        increase_interval=None
):
    """
    Runs a performance test with the provided configuration.

    Args:
        test_data: Data to be used for the test.
        test_duration_secs: Optional duration of the test in seconds.
        concurrent_requests: Optional number of concurrent requests.
        timeout_secs: Optional timeout in seconds for individual requests.
        cookie_store_enable: Optional flag to enable cookie storage.
        verbose: Optional flag to enable verbose logging.
        increase_step: Optional step size for increasing load (experimental).
        increase_interval: Optional interval for load increase (experimental).

    Returns:
        An object representing the test runner (implementation-specific).
    """
    try:
        engine = AtomicBombEngine(
            test_duration_secs=test_duration_secs,
            concurrent_requests=concurrent_requests,
            timeout_secs=timeout_secs,
            cookie_store_enable=cookie_store_enable,
            verbose=verbose,
            increase_step=increase_step,
            increase_interval=increase_interval,
        )
        runner = engine.run(test_data)
        return runner
    except (Exception, KeyboardInterrupt):
        raise Exception("Test runner encountered an exception.")
