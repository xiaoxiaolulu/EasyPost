import json
import os
from urllib.parse import (
    urljoin,
    urlparse
)
from utils.logger import logger
from utils.recursion import GetJsonParams


class DataSource:

    def connect(self):
        ...

    def read(self, filename):
        ...

    def write(self, ctx):
        ...


class SwaggerDataSource(DataSource):

    def __init__(self):
        self.case_list: list = []

    @staticmethod
    def load(filepath):
        """
        Loads the content of a file and returns it.

        Args:
            filepath (str): The path to the file.

        Returns:
            object: The content of the file,
                    as a dictionary if it's a JSON file,
                    or an empty string on errors.

        Raises:
            FileExistsError: If the specified file doesn't exist.
            FileNotFoundError: If the file path is invalid or the file cannot be opened.
            AttributeError: If there's an error parsing the JSON content.
        """
        try:
            suffix = os.path.splitext(filepath)[-1]
            if suffix not in [".json"]:
                return "必须上传 (*.json) 后缀的文件"

            with open(filepath, 'r', encoding="utf-8") as stream:
                content = json.load(stream)
                return content

        except (FileExistsError, FileNotFoundError, AttributeError):
            filename = os.path.basename(filepath)
            return f"文件 {filename} 不存在，请检查!"

    def prepare_test_steps(self, t_collection):
        """
        Prepares individual test steps based on a provided test collection.

        Args:
            t_collection (dict): A dictionary representing the test collection data.

        Raises:
            (Exception): Potential exceptions from underlying methods.
        """
        severs = self.make_request_servers(t_collection)

        for item in t_collection.get("paths").keys():
            main = GetJsonParams.get_value(t_collection, item)
            case = self.prepare_test_step(t_collection, main, severs, item)
            self.case_list.append(case)

    def prepare_test_step(self, t_collection, main, severs, item):
        """
        Prepares a single test step dictionary based on provided data.

        Args:
            t_collection (dict): The overall test collection data.
            main (dict): The main test case data for the current path.
            severs (dict): (Optional) Servers dictionary for request servers.
            item (str): The API endpoint name (key) from the collection.

        Returns:
            dict: A dictionary representing a single test step with details.
        """
        return {
            'name': self.make_request_remarks(main),
            'method': self.make_request_method(main),
            'url': self.make_request_url(severs, item),
            'desc': self.make_request_remarks(main),
            'headers': self.make_request_headers(main),
            'raw': self.make_request_body(t_collection, main)
        }

    def make_request_body(self, t_collection, main):
        """
        Constructs the request body based on content type and data from test collection.

        Args:
            test_collection (dict): The overall test collection data.
            main (dict): The main test case data for the current path.

        Returns:
            dict: A dictionary representing the request body structure.

        Raises:
            ValueError: If an unsupported content type is encountered.
        """
        headers = self.make_request_headers(main)
        content_type = headers.pop().get('Content-Type')

        if content_type == "multipart/form-data":
            return {"form_data": self.make_request_content(t_collection, main)}
        if content_type == "application/json":
            return {"json": {content.get('name', ''): "" for content in self.make_request_content(t_collection, main)}}
        if content_type == "x_www_form_urlencoded":
            return {"x_www_form_urlencoded": self.make_request_content(t_collection, main)}
        else:
            return {"data": {}}

    @staticmethod
    def make_request_content(t_collection, main):
        """
        Extracts request content parameters from test case data.

        Args:
            t_collection (dict): The overall test collection data.
            main (dict): The main test case data for the current path.

        Returns:
            list: A list of dictionaries representing request content parameters.

        Raises:
            KeyError: If a required key is missing in the test data.
        """

        try:
            parameters = GetJsonParams.get_value(main, "parameters")
            parameters = [
                {"name": p["name"], "value": "", "description": p.get("description", ""), "type": p.get("type", "")}
                for p in parameters
            ]

        except (KeyError, AttributeError, TypeError):
            try:
                schema = GetJsonParams.get_value(main, "schema")
                req_object = str(list(schema.values()).pop()).split("/")[-1]
                parameters = GetJsonParams.get_value(t_collection, req_object)

                parameters = [
                    {"name": k, "value": "", "description": v.get("description", ""), "type": v.get("type", "")}
                    for k, v in GetJsonParams.get_value(parameters, "properties").items()
                ]
            except (KeyError, AttributeError):
                raise KeyError("Missing or invalid request content data")

        return parameters

    @staticmethod
    def make_request_method(main):
        """
        Extracts the HTTP request method from the main test case data.

        Args:
            main (dict): The main test case data for the current path.

        Returns:
            str: The HTTP request method (e.g., GET, POST).

        Raises:
            KeyError: If the main data doesn't contain a request method.
        """
        method = list(main.keys()).pop()
        return method

    @staticmethod
    def make_request_servers(t_collection):
        """
        Extracts the base URL for requests from the test collection data.

        Args:
            t_collection (dict): The overall test collection data.

        Returns:
            str: The base URL for requests (if present).

        Raises:
            KeyError: If the "servers" or "url" key is missing in the test collection data.
        """

        try:
            servers = t_collection.get('servers')
            if not servers:
                raise KeyError

            return GetJsonParams.get_value(servers, 'url')

        except KeyError:
            # Raise a specific error if base URL is missing
            return f"http://{GetJsonParams.get_value(t_collection, 'host')}"

    @staticmethod
    def make_request_remarks(main):
        """
        Extracts remarks (description or summary) from the main test case data.

        Args:
            main (dict): The main test case data for the current path.

        Returns:
            str: The extracted remarks (if present, otherwise an empty string).
        """
        description = GetJsonParams.get_value(main, "summary")
        return description

    @staticmethod
    def make_request_headers(main):
        """
        Constructs request headers, primarily focusing on the Content-Type header.

        Args:
            main (dict): The main test case data for the current path.

        Returns:
            list: A list of dictionaries representing request headers.
        """
        try:
            header_value = GetJsonParams.get_value(main, 'consumes').pop()
        except AttributeError:
            header_value = ""

        headers = [{"name": "Content-Type", "value": header_value, "description": "1"}]
        return headers

    @staticmethod
    def make_request_url(severs, item):
        """
        Constructs the complete request URL by combining base URL and API endpoint path.

        Args:
            severs (str): The base URL for requests (potentially from servers dictionary).
            item (str): The API endpoint path (key) from the test collection.

        Returns:
            str: The complete and validated request URL.

        Raises:
            ValueError: If the URL parsing fails.
        """
        raw_url = urljoin(severs, item)
        try:
            u = urlparse(raw_url)
            return f"{u.scheme}://{u.netloc}{u.path}"
        except (Exception, ):
            logger.error('parse URL error')

    def connect(self):
        pass

    def read(self, filename):
        """
        Reads and processes a Swagger file.

        Args:
            filename (str): The path to the Swagger file.

        Returns:
            dict: A dictionary representing the prepared test steps based on the Swagger data.

        Raises:
            Exception: Potential exceptions from underlying methods (load, prepare_test_steps).
        """
        swagger_content = self.load(filename)
        self.prepare_test_steps(swagger_content)
        prepare_content = self.case_list
        return prepare_content

    def write(self, ctx):
        pass


class UitRunnerSource(DataSource):
    def connect(self):
        pass

    def read(self, filename):
        pass

    def write(self, ctx):
        print(ctx)


class DataMigrator:
    def __init__(self, source: DataSource, target: DataSource):
        self.source = source
        self.target = target

    def migrate(self, request=None, pk=None):
        ctx = self.source.read('middle.json')
        self.target.write(ctx)


if __name__ == '__main__':
    migrator = DataMigrator(SwaggerDataSource(), UitRunnerSource())
    migrator.migrate()
