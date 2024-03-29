import base64
import random
import string
import time
import rsa
from faker import Faker
from utils.time import *

__all__ = [
    "now_time",
    "current_date",
    "day_num",
    "week_start",
    "week_end",
    "week_end",
    "month_start",
    "month_end",
    "yesterday",
    "get_before_day",
    "random_mobile",
    "random_name",
    "random_ssn",
    "random_addr",
    "random_city",
    "random_company",
    "random_postcode",
    "random_email",
    "random_date",
    "random_ipv4",
    "random_date_time",
    "get_timestamp",
    "base64_encode",
    "md5_encrypt",
    "rsa_encrypt",
    "random_float",
    "random_natural",
    "random_character",
    "random_string",
    "array_range",
    "guid",
    "url",
    "postcode",
    "paragraph",
    "title",
    "get_time_stamp"
]


fk = Faker(locale='zh_CN')


def random_mobile():
    """
    Generates a random mobile phone number.

    This function uses the `fk.phone_number()` function from the Faker library to generate a random mobile phone number.

    Args:
        None

    Returns:
        A randomly generated mobile phone number (string).
    """
    return fk.phone_number()


def random_name():
    """
    Generates a random name.

    This function uses the `fk.name()` function from the Faker library to generate a random name.

    Args:
        None

    Returns:
        A randomly generated name (string).
    """
    return fk.name()


def random_ssn():
    """
    Generates a random Social Security number (SSN).

    This function uses the `fk.ssn()` function from the Faker library to generate a random SSN.

    Args:
        None

    Returns:
        A randomly generated SSN (string).
    """
    return fk.ssn()


def random_addr():
    """
    Generates a random address.

    This function uses the `fk.address()` function from the Faker library to generate a random address.

    Args:
        None

    Returns:
        A randomly generated address (string).
    """
    return fk.address()


def random_city():
    """
       Generates a random city name.

       This function uses the `fk.city()` function from the Faker library to generate a random city name.

       Args:
           None

       Returns:
           A randomly generated city name (string).
    """
    return fk.city()


def random_company():
    """
    Generates a random company name.

    This function uses the `fk.company()` function from the Faker library to generate a random company name.

    Args:
        None

    Returns:
        A randomly generated company name (string).
    """
    return fk.company()


def random_postcode():
    """
        Generates a random postcode.

        This function uses the `fk.postcode()` function from the Faker library to generate a random postcode.

        Args:
            None

        Returns:
            A randomly generated postcode (string).
    """
    return fk.postcode()


def random_email():
    """
    Generates a random email address.

    This function uses the `fk.email()` function from the Faker library to generate a random email address.

    Args:
        None

    Returns:
        A randomly generated email address (string).
    """
    return fk.email()


def random_date():
    """
    Generates a random date.

    This function uses the `fk.date()` function from the Faker library to generate a random date.

    Args:
        None

    Returns:
        A randomly generated date (string).
    """
    return fk.date()


def random_date_time():
    """
     Generates a random date and time.

     This function uses the `fk.date_time()` function from the Faker library to generate a random date and time.

     Args:
         None

     Returns:
         A randomly generated date and time (string).
    """
    return fk.date_time()


def random_natural():
    """
       Generates a random natural number.

       This function uses the `fk.random_int()` function from the Faker library to generate
       a random natural number between 1 and 100.

       Args:
           None

       Returns:
           A randomly generated natural number (integer).
    """
    random_number = fk.random_int(min=1, max=100, step=1)
    return random_number


def random_float():
    """
       Generates a random float number.

       This function uses the `fk.pyfloat()` function from the Faker library
       to generate a random float number between 0 and 100.

       Args:
           None

       Returns:
           A randomly generated float number (float).
    """
    random_number = round(fk.pyfloat(min_value=0, max_value=100), 2)
    return random_number


def random_character():
    """
    Generates a random character.

    This function uses the `fk.lexify()` function from the Faker library to generate a random character.

    Args:
        None

    Returns:
        A randomly generated character (string).
    """
    character = fk.lexify()
    return character


def random_string():
    """
    Generates a random string of lowercase letters.

    This function generates a random string of lowercase letters with a length between 1 and 10 characters.

    Args:
        None

    Returns:
        A randomly generated string (string).
    """
    string_pool = list(string.ascii_lowercase)
    ret_string = "".join(fk.random_sample(elements=string_pool, length=random.randint(1, 10)))
    return ret_string


def array_range(start, stop, step):
    """
    Generates an array of random integers within a specified range.

    This function generates an array of `stop // step` random integers between
    `start` (inclusive) and `stop` (exclusive) with a step of `step`.

    Args:
        start (int): The starting value (inclusive) for the random integers.
        stop (int): The ending value (exclusive) for the random integers. Must be greater than `start`.
        step (int, optional): The step value between consecutive elements. Defaults to 1.

    Returns:
        list: An array of randomly generated integers.
    """
    random_array = [fk.random_int(min=start, max=stop, step=step) for _ in range(stop // step)]
    return random_array


def guid():
    """
    Generates a random Universally Unique Identifier (UUID).

    This function uses the `fk.uuid4` function from the Faker library to generate a random UUID.

    Args:
        None

    Returns:
        str: A randomly generated UUID (string).
    """
    return fk.uuid4()


def url():
    """
    Generates a random URL.

    This function uses the `fk.url` function from the Faker library to generate a random URL.

    Args:
        None

    Returns:
        str: A randomly generated URL (string).
    """
    return fk.url()


def postcode():
    """
    Generates a random postcode.

    This function uses the `fk.postcode` function from the Faker library to generate a random postcode.

    Args:
        None

    Returns:
        str: A randomly generated postcode (string).
    """
    return fk.postcode()


def paragraph():
    """
    Generates a random paragraph of text.

    This function uses the `fk.text` function from the Faker library to generate a random paragraph of text.

    Args:
        None

    Returns:
        str: A randomly generated paragraph of text (string).
    """
    return fk.text()


def title():
    """
    Generates a random title.

    This function uses the `fk.sentence` function from the Faker library to generate a random title.

    Args:
        None

    Returns:
        str: A randomly generated title (string).
    """
    return fk.sentence(nb_words=4)


def random_ipv4():
    """
    Generates a random IPv4 address.

    This function uses the `fk.ipv4` function from the Faker library to generate a random IPv4 address.

    Args:
        None

    Returns:
        str: A randomly generated IPv4 address (string).
    """
    return fk.ipv4()


def get_timestamp():
    """
    Gets the current timestamp.

    This function uses the `time.time()` function to get the current timestamp, which is the number of seconds since the Unix epoch.

    Args:
        None

    Returns:
        float: The current timestamp (number of seconds since the Unix epoch).
    """
    return time.time()


def base64_encode(data: str):
    """
    Encodes data with base64.

    Args:
        data: The string to encode.

    Returns:
        str: The encoded string.
    """
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def md5_encrypt(data: str):
    """
    Encrypts data with MD5.

    Args:
        data: The string to encrypt.

    Returns:
        str: The encrypted string.
    """
    from hashlib import md5
    new_md5 = md5()
    new_md5.update(data.encode('utf-8'))
    return new_md5.hexdigest()


def rsa_encrypt(msg, server_pub):
    """
    Encrypts a message using RSA encryption.

    Args:
        msg (str): The message to encrypt.
        server_pub (str): The server's public key in PEM format.

    Returns:
        str: The base64-encoded encrypted message.
    """
    msg = msg.encode('utf-8')
    pub_key = server_pub.encode("utf-8")
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
    cryto_msg = rsa.encrypt(msg, public_key_obj)
    cipher_base64 = base64.b64encode(cryto_msg)
    return cipher_base64.decode()


def get_time_stamp(str_len=13):
    """
    Gets a timestamp with a specified length.

    This function generates a timestamp string representing the current time since the Unix epoch.
    The user can optionally specify the desired length of the timestamp string.

    Args:
        str_len (int, optional): The desired length of the timestamp string. Defaults to 13 (represents milliseconds).
            Must be an integer between 1 and 16 (inclusive).

    Returns:
        str: The timestamp string with the specified length.

    Raises:
        Exception: If the provided `str_len` is not an integer between 1 and 16 (inclusive).
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]

    raise Exception("timestamp length can only between 0 and 16.")
