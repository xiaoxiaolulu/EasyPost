import json

from utils.logger import logger


def read_json_file(file_path):
    """Reads a JSON file and returns the parsed data.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        any: The parsed data from the JSON file.

    Raises:
        FileNotFoundError: If the file is not found.
        json.JSONDecodeError: If the JSON data is invalid.
    """

    try:
        with open(file_path, 'r', encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON data in file: {file_path}")


def get_suites(data):
    """Extracts the 'suites' data from the parsed JSON content.

    Args:
        data (any): The parsed JSON data.

    Returns:
        list: A list of suites extracted from the data.

    Raises:
        KeyError: If the expected keys are not found in the JSON data.
    """

    try:
        return data["results"][-1]["suites"]
    except KeyError as e:
        raise KeyError(f"Missing required keys in JSON data: {e}")


def get_step_info(step):
    """Extracts context and error message (if any) from a test step.

    Args:
        step (dict): A dictionary representing a test step.

    Returns:
        tuple: A tuple containing (context, error_message).
    """

    context = step.get("context")
    error_message = step.get("err", {}).get("message")
    return context, error_message


def print_step_info(step):
    """Prints the context and error message (if any) of a test step.

    Args:
        step (dict): A dictionary representing a test step.
    """

    context, error_message = get_step_info(step)
    return context, error_message


def main():
    """The main function that reads the JSON file, processes data, and prints step information."""

    try:
        collections = []
        content = read_json_file("mochawesome.json")
        suites = get_suites(content)
        for suite in suites:

            for i, step in enumerate(suite["tests"], 1):
                context, error_message = print_step_info(step)
                context = eval(context)

                collections.append({
                    "steps": [x + ("×" if (i == len(context) - 2 and context[-1].endswith(".png")) else "√")
                              for i, x in enumerate(context)
                              if not (i == len(context) - 1 and str(x).endswith(".png"))],
                    "screenshot": context.pop() if context.pop().__contains__("png") else "",
                    "error_message": error_message
                })
        return collections
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    print(main())
    # for value in main():
    #     print(value)
