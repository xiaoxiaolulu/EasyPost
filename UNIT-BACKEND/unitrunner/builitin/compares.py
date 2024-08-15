"""
Built-in validate comparators.
"""
import re
import typing
from api.events.registry import registry


@registry.register("相等")
def equal(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    """
    This function compares two values and raises an assertion error if they are not equal.

    Args:
        check_value: The value to be checked against the expected value.
        expect_value: The expected value.
        message: An optional message to be included in the assertion error if the values are not equal.

    Raises:
        AssertionError: If the check_value is not equal to the expect_value.
    """
    assert check_value == expect_value, message


@registry.register("大于")
def greater_than(
    check_value: typing.Union[int, float], expect_value: typing.Union[int, float], message: str = ""
):
    """
    This function compares two numeric values and raises an assertion error if the check_value is not greater than the expected value.

    Args:
        check_value: The numeric value to be checked against the expected value. Must be either an integer or a float.
        expect_value: The expected numeric value. Must be either an integer or a float.
        message: An optional message to be included in the assertion error if the check_value is not greater than the expected value.

    Raises:
        AssertionError: If the check_value is not greater than the expected value.
    """
    assert check_value > expect_value, message


@registry.register("小于")
def less_than(
    check_value: typing.Union[int, float], expect_value: typing.Union[int, float], message: str = ""
):
    """
    Checks if a value is less than an expected value and raises an assertion error if not.

    Args:
        check_value: The value to be checked for being less than (int or float).
        expect_value: The expected value to compare against (int or float).
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If check_value is not less than expect_value.
    """
    assert check_value < expect_value, message


@registry.register("大于等于")
def greater_or_equals(
    check_value: typing.Union[int, float], expect_value: typing.Union[int, float], message: str = ""
):
    """
    Compares two numeric values and raises an assertion error if the check_value is not greater than or equal to the expected value.

    Args:
        check_value: The numeric value to be checked against the expected value. Must be either an integer or a float.
        expect_value: The expected numeric value. Must be either an integer or a float.
        message: An optional message to be included in the assertion error if the check_value is not greater than or equal to the expected value.

    Raises:
        AssertionError: If the check_value is less than the expected value.
    """
    assert check_value >= expect_value, message


@registry.register("小于等于")
def less_or_equals(
    check_value: typing.Union[int, float], expect_value: typing.Union[int, float], message: str = ""
):
    """
    Checks if a value is less than or equal to an expected value and raises an assertion error if not.

    Args:
        check_value: The value to be checked (must be an integer or float).
        expect_value: The expected value to compare against (must be an integer or float).
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If check_value is greater than expect_value.
    """
    assert check_value <= expect_value, message


@registry.register("不等于")
def not_equal(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    """
    Asserts that two values are not equal, raising an AssertionError if they are equal.

    Args:
        check_value: The value to be checked for inequality.
        expect_value: The value that check_value should not be equal to.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If check_value is equal to expect_value.
    """
    assert check_value != expect_value, message


@registry.register("不为空")
def not_none(check_value: typing.Any, expect_value: typing.Any = None, message: str = ""):
    """
    Asserts that a value is not None and not an empty string, raising an AssertionError if either condition is not met.

    Args:
        check_value: The value to be checked for not being None or an empty string.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If check_value is None or an empty string.
    """
    assert check_value is not None or check_value != "", message


@registry.register("为空")
def is_none(check_value: typing.Any, expect_value: typing.Any = None, message: str = ""):
    """
    Asserts that a value is None or an empty string, raising an AssertionError if not.

    Args:
        check_value: The value to be checked for being None or an empty string.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If check_value is not None or an empty string.
    """
    assert check_value is None or check_value == "", message


@registry.register("字符串类型相等")
def string_equals(check_value: str, expect_value: typing.Any, message: str = ""):
    """
    Asserts that the string representation of a value is equal to an expected string, raising an AssertionError if not.

    Args:
        check_value: The value to be checked, which must be a string.
        expect_value: The expected value to compare against, which can be of any type. It will be converted to a string for comparison.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If the string representation of check_value is not equal to the string representation of expect_value.
    """
    assert str(check_value) == str(expect_value), message


@registry.register("长度相等")
def length_equal(check_value: str, expect_value: int, message: str = ""):
    """
    Asserts that the length of a string is equal to an expected integer value, raising Assertions if conditions aren't met.

    Args:
        check_value: The string to check its length.
        expect_value: The expected integer value for the string length.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If either:
            - expect_value is not of type integer.
            - The length of check_value is not equal to expect_value.
    """
    assert isinstance(expect_value, int), "expect_value should be int type"
    assert len(check_value) == expect_value, message


@registry.register("长度大于")
def length_greater_than(
    check_value: str, expect_value: typing.Union[int, float], message: str = ""
):
    """
        Asserts that the length of a string is greater than an expected numeric value, raising Assertions if conditions aren't met.

        Args:
            check_value: The string to check its length.
            expect_value: The expected numeric value (int or float) to compare against the string length.
            message: An optional message to include in the assertion error if raised.

        Raises:
            AssertionError: If either:
                - expect_value is not of type integer or float.
                - The length of check_value is not greater than expect_value.
    """
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value should be int/float type"
    assert len(check_value) > expect_value, message


@registry.register("长度大于等于")
def length_greater_or_equals(
    check_value: str, expect_value: typing.Union[int, float], message: str = ""
):
    """
    Asserts that the length of a string is greater than or equal to an expected numeric value, raising Assertions if conditions aren't met.

    Args:
        check_value: The string to check its length.
        expect_value: The expected numeric value (int or float) to compare against the string length.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If either:
            - expect_value is not of type integer or float.
            - The length of check_value is less than expect_value.
    """
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value should be int/float type"
    assert len(check_value) >= expect_value, message


@registry.register("长度小于")
def length_less_than(
    check_value: str, expect_value: typing.Union[int, float], message: str = ""
):
    """
    Asserts that the length of a string is less than an expected numeric value, raising Assertions if conditions aren't met.

    Args:
        check_value: The string to check its length.
        expect_value: The expected numeric value (int or float) to compare against the string length.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If either:
            - expect_value is not of type integer or float.
            - The length of check_value is not less than expect_value.
    """
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value should be int/float type"
    assert len(check_value) < expect_value, message


@registry.register("长度小于等于")
def length_less_or_equals(
    check_value: str, expect_value: typing.Union[int, float], message: str = ""
):
    """
    Asserts that the length of a string is less than or equal to an expected numeric value, raising Assertions if conditions aren't met.

    Args:
        check_value: The string to check its length.
        expect_value: The expected numeric value (int or float) to compare against the string length.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If either:
            - expect_value is not of type integer or float.
            - The length of check_value is greater than expect_value.
    """
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value should be int/float type"
    assert len(check_value) <= expect_value, message


@registry.register("包含")
def contains(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    assert isinstance(
        check_value, (list, tuple, dict, str, bytes)
    ), "expect_value should be list/tuple/dict/str/bytes type"
    """
    Asserts that an expected value is contained within a collection or string-like value, raising Assertions if conditions aren't met.

    Args:
        check_value: The collection or string-like value to check for containment.
        expect_value: The value to search for within check_value.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If either:
            - check_value is not a list, tuple, dict, string, or bytes.
            - expect_value is not found within check_value.
    """
    assert expect_value in check_value, message


@registry.register("包含常见类型")
def contained_by(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    assert isinstance(
        expect_value, (list, tuple, dict, str, bytes)
    ), "expect_value should be list/tuple/dict/str/bytes type"
    """
        Asserts that a value is contained within an expected collection or string-like value, raising Assertions if conditions aren't met.

        Args:
            check_value: The value to check if it's contained within expect_value.
            expect_value: The collection or string-like value to search for check_value within.
            message: An optional message to include in the assertion error if raised.

        Raises:
            AssertionError: If either:
                - expect_value is not a list, tuple, dict, string, or bytes.
                - check_value is not found within expect_value.
    """
    assert check_value in expect_value, message


@registry.register("类型匹配")
def type_match(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    """
        Asserts that a value has the expected type, handling NoneType explicitly and allowing type names as strings for flexibility.

        Args:
            check_value: The value to check its type.
            expect_value: The expected type, either a type object or a string representation of the type.
            message: An optional message to include in the assertion error if raised.

        Raises:
            AssertionError: If the type of check_value is not the same as the specified expect_value.
            ValueError: If expect_value is not a valid type or type name.
    """
    def get_type(name):
        if isinstance(name, type):
            return name
        elif isinstance(name, str):
            try:
                return __builtins__[name]
            except KeyError:
                raise ValueError(name)
        else:
            raise ValueError(name)

    if expect_value in ["None", "NoneType", None]:
        assert check_value is None, message
    else:
        assert type(check_value) == get_type(expect_value), message


@registry.register("正则匹配")
def regex_match(check_value: str, expect_value: typing.Any, message: str = ""):
    """
        Asserts that a string value matches a specified regular expression pattern, raising Assertions if conditions aren't met.

        Args:
            check_value: The string to check for a match against the regular expression.
            expect_value: The regular expression pattern as a string.
            message: An optional message to include in the assertion error if raised.

        Raises:
            AssertionError: If either:
                - expect_value is not a string.
                - check_value is not a string.
                - check_value does not match the regular expression pattern.
    """
    assert isinstance(expect_value, str), "expect_value should be Text type"
    assert isinstance(check_value, str), "check_value should be Text type"
    assert re.match(expect_value, check_value), message


@registry.register("前缀相等")
def startswith(check_value: typing.Any, expect_value: typing.Any, message: str = ""):
    """
    Asserts that a string representation of a value starts with a specified prefix, raising Assertions if conditions aren't met.

    Args:
        check_value: The value to be checked for starting with the prefix.
        expect_value: The expected prefix string.
        message: An optional message to include in the assertion error if raised.

    Raises:
        AssertionError: If the string representation of check_value does not start with expect_value.
    """
    assert str(check_value).startswith(str(expect_value)), message


@registry.register("后缀相等")
def endswith(check_value: str, expect_value: typing.Any, message: str = ""):
    """
        Asserts that a string value ends with a specified suffix, ensuring string conversion for both values.

        Args:
            check_value: The string value to be checked for the ending suffix.
            expect_value: The expected suffix value (will be converted to a string).
            message: An optional message to include in the assertion error if raised.

        Raises:
            AssertionError: If check_value does not end with the string representation of expect_value.
    """
    assert str(check_value).endswith(str(expect_value)), message
