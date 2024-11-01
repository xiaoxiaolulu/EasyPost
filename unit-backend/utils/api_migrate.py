import json
import os
from urllib.parse import (
    urljoin,
    urlparse
)
from api.emus.ApiParametersEnum import (
    ApiHeadersEnum,
    ApiModeEnum
)
from api.events.registry import registry
from api.models.https import Api
from api.models.project import Project
from utils.logger import logger
from utils.recursion import GetJsonParams


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


class DataSource:

    def connect(self):
        ...

    def read(self, filename):
        ...

    def write(self, ctx):
        ...


@registry.register("swagger")
class SwaggerDataSource(DataSource):

    def __init__(self):
        self.case_list: list = []

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
            severs (dict): (Optional) Servers dictionary for process servers.
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
        Constructs the process body based on content type and data from test collection.

        Args:
            test_collection (dict): The overall test collection data.
            main (dict): The main test case data for the current path.

        Returns:
            dict: A dictionary representing the process body structure.

        Raises:
            ValueError: If an unsupported content type is encountered.
        """
        headers = self.make_request_headers(main)
        content_type = headers.pop().get('Content-Type')

        if content_type == ApiHeadersEnum.FORM_DATA:
            return {"form_data": self.make_request_content(t_collection, main)}
        if content_type == ApiHeadersEnum.JSON:
            return {"json": {content.get('name', ''): "" for content in self.make_request_content(t_collection, main)}}
        if content_type == ApiHeadersEnum.X_WWW_FORM_URLENCODED:
            return {"x_www_form_urlencoded": self.make_request_content(t_collection, main)}
        else:
            return {"data": {}}

    @staticmethod
    def make_request_content(t_collection, main):
        """
        Extracts process content parameters from test case data.

        Args:
            t_collection (dict): The overall test collection data.
            main (dict): The main test case data for the current path.

        Returns:
            list: A list of dictionaries representing process content parameters.

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
                raise KeyError("Missing or invalid process content data")

        return parameters

    @staticmethod
    def make_request_method(main):
        """
        Extracts the HTTP process method from the main test case data.

        Args:
            main (dict): The main test case data for the current path.

        Returns:
            str: The HTTP process method (e.g., GET, POST).

        Raises:
            KeyError: If the main data doesn't contain a process method.
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
        Constructs process headers, primarily focusing on the Content-Type header.

        Args:
            main (dict): The main test case data for the current path.

        Returns:
            list: A list of dictionaries representing process headers.
        """
        try:
            header_value = GetJsonParams.get_value(main, 'consumes').pop()
        except AttributeError:
            header_value = ""

        headers = [{"name": "Content-Type", "value": header_value, "description": ""}]
        return headers

    @staticmethod
    def make_request_url(severs, item):
        """
        Constructs the complete process URL by combining base URL and API endpoint path.

        Args:
            severs (str): The base URL for requests (potentially from servers dictionary).
            item (str): The API endpoint path (key) from the test collection.

        Returns:
            str: The complete and validated process URL.

        Raises:
            ValueError: If the URL parsing fails.
        """
        raw_url = urljoin(severs, item)
        try:
            u = urlparse(raw_url)
            return f"{u.scheme}://{u.netloc}{u.path}"
        except (Exception,):
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
        swagger_content = load(filename)
        self.prepare_test_steps(swagger_content)
        prepare_content = self.case_list
        return prepare_content

    def write(self, ctx):
        pass


@registry.register("postman")
class PostManDataSource(DataSource):

    def __init__(self):
        self.case_list = []

    def prepare_test_steps(self, t_collection):
        """
        Prepares individual test steps from a test collection.

        Args:
            t_collection (dict): The dictionary representing the test collection data.

        Returns:
            None
        """
        for item in t_collection.get('item'):
            case = self.prepare_test_step(item)
            self.case_list.append(case)

    def prepare_test_step(self, item):
        """
        Prepares a dictionary representing a single test step from a test item.

        Args:
            item (dict): A dictionary representing a test item from the test collection.

        Returns:
            dict: A dictionary containing information for the prepared test step.
        """

        return {
            'name': self.make_request_remarks(item),
            'method': self.make_request_method(item),
            'url': self.make_request_url(item),
            'desc': self.make_request_remarks(item),
            'headers': self.make_request_headers(item),
            'raw': self.make_request_body(item)
        }

    @staticmethod
    def make_request_body(item):
        request_body = GetJsonParams.get_value(item, 'body')

        if request_body.get('mode') == ApiModeEnum.FORM_DATA:
            return {"form_data": [{"name": p["key"], "value": p["value"], "description": "", "type": p.get("type", "")}
                                  for p in request_body.get('formdata')]}
        if request_body.get('mode') == ApiModeEnum.X_WWW_FORM_URLENCODED:
            return {"x_www_form_urlencoded": [
                {"name": p["key"], "value": p["value"], "description": "", "type": p.get("type", "")}
                for p in request_body.get('formdata')]}
        if request_body.get("mode") == ApiModeEnum.RAW:
            return {"json": {request_body.get("raw")}}
        else:
            return {"data": {}}

    def make_request_body(self, item):
        """
        Constructs the process body based on the body definition in the test item.

        Args:
            item (dict): A dictionary representing a test item from the test collection.

        Returns:
            dict: A dictionary representing the process body structure.

        Raises:
            ValueError: If an unsupported process body mode is encountered.
        """

        request_body = GetJsonParams.get_value(item, 'body')

        # Use a dictionary lookup for body mode handling
        body_builders = {
            "formdata": self._build_form_data,
            "x-www-form-urlencoded": self._build_form_data,  # Consider separate handling if needed
            "raw": self._build_raw_body,
        }

        try:
            # Get the body mode and its corresponding builder function
            body_mode = request_body.get('mode')
            build_body_func = body_builders.get(body_mode)

            # Validate and build the process body using the appropriate function
            if build_body_func:
                return build_body_func(request_body)
            else:
                raise ValueError(f"Unsupported process body mode: {body_mode}")

        except (AttributeError, KeyError) as e:
            # Handle potential errors like missing keys or attributes
            logger.warning(f"Error processing process body data: {e}")
            return {"data": {}}

    @staticmethod
    def _build_form_data(request_body):
        """
        Builds a dictionary representing form data based on the provided data.

        Args:
            request_body (dict): The process body dictionary containing form data information.

        Returns:
            dict: A dictionary representing the form data structure.
        """

        return {"form_data": [{"name": p["key"], "value": p["value"], "description": "", "type": p.get("type", "")}
                              for p in request_body.get('formdata')]}

    @staticmethod
    def _build_raw_body(request_body):
        """
        Builds a dictionary representing a raw process body based on the provided data.

        Args:
            request_body (dict): The process body dictionary containing raw data.

        Returns:
            dict: A dictionary representing the raw process body structure.
        """

        return {"json": {request_body.get("raw")}}

    @staticmethod
    def make_request_remarks(item):
        """
        Generates remarks for a test step based on the provided item.

        Args:
            item (dict): A dictionary representing a test item from the test collection.

        Returns:
            str: The remarks string for the test step.
        """
        name = item.get('name', '')
        return name

    @staticmethod
    def make_request_method(item):
        """
        Extracts the process method from the test item.

        Args:
            item (dict): A dictionary representing a test item from the test collection.

        Returns:
            str: The process method (e.g., GET, POST, etc.).
        """
        method = GetJsonParams.get_value(item, 'method')
        return method

    @staticmethod
    def make_request_url(item):
        """
        Extracts the process URL from the test item.

        Args:
            item (dict): A dictionary representing a test item from the test collection.

        Returns:
            str: The process URL.
        """
        url = GetJsonParams.get_value(item, 'url').get('raw', '')
        return url

    @staticmethod
    def make_request_headers(item):
        """
        Constructs process headers based on the header definition in the test item.

        Args:
            item (dict): A dictionary representing a test item from the test collection.

        Returns:
            list: A list of dictionaries representing process headers (empty list if no headers defined).
        """

        try:
            header_data = GetJsonParams.get_value(item, 'header')

            if header_data:
                headers = [
                    {"name": h.get('key', ''), "value": h.get('value', ''), "description": ""}
                    for h in header_data
                ]
                return headers

        except AttributeError as e:
            logger.warning(f"Error processing process header data: {e}")

        return []

    def read(self, filename):
        """
        Reads a Postman collection file and prepares test steps from its content.

        Args:
            filename (str): The path to the Postman collection file.

        Returns:
            list: A list of dictionaries representing the prepared test steps.
        """
        postman_content = load(filename)
        self.prepare_test_steps(postman_content)
        return self.case_list


class UitRunnerSource(DataSource):

    def connect(self):
        pass

    def read(self, filename):
        pass

    def write(self, context):
        """
        Writes test case data to the database.

        Args:
            context (list): A list of dictionaries representing individual test cases.

        Raises:
            Exception: If any data insertion fails due to missing objects or other errors.
        """

        for ctx in context:
            try:
                project = Project.objects.get(id=ctx.get('pk'))
                Api.objects.create(
                    name=ctx.get("name"),
                    priority=1,
                    project=project,
                    directory_id=1,
                    status=0,
                    method=ctx.get('method'),
                    url=ctx.get('url'),
                    desc=ctx.get('desc'),
                    headers=ctx.get('headers', {}),
                    params="",
                    raw=ctx.get('raw'),
                    setup_script="",
                    teardown_script="",
                    validate="",
                    extract="",
                    source=ctx.get("type"),
                    user=ctx.get('process').user
                )

            except (Api.DoesNotExist, Project.DoesNotExist) as e:
                logger.error(f"Error creating API object: {ctx.get('name')} - {e}")
                raise ValueError(f"Project or API data not found for test case: {ctx.get('name')}")
            except Exception as e:
                logger.exception(f"Unexpected error writing test case data: {e}")
                raise Exception("An error occurred while importing test cases.")


class DataMigrator:
    def __init__(self, source: DataSource, target: DataSource):
        self.source = source
        self.target = target

    def migrate(self, filename=None, request=None, pk=None, type=None):
        """
        Migrates test case data from source to target.

        Args:
            type: file type to migrate
            filename: filepath
            request (HttpRequest, optional): The Django process object (if applicable).
            pk (int, optional): Primary key of the project (if applicable).

        Raises:
            Exception: If any errors occur during data reading or writing.
        """

        try:
            # Read test case data from the source (assuming 'middle.json')
            ctx = self.source.read(filename)
            # Add process and pk information to each context dictionary
            ctx = [
                {**c, **{'process': request, 'pk': pk, "type": type}} for c in ctx
            ]

            self.target.write(ctx)

        except Exception as e:
            logger.exception(f"Error migrating test case data: {e}")
            raise Exception("An error occurred while migrating test cases.")


if __name__ == '__main__':
    migrator = DataMigrator(SwaggerDataSource(), UitRunnerSource())
    migrator.migrate()
