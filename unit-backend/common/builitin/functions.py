import base64
import random
import string
import time
import rsa
from faker import Faker
from common import exceptions
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
    返回一个随机的手机号
    """
    return fk.phone_number()


def random_name():
    """
    生成一个随机的名字
    """
    return fk.name()


def random_ssn():
    """
    生成一个随机的社会安全号码(SSN)。
    """
    return fk.ssn()


def random_addr():
    """
    生成随机地址.
    """
    return fk.address()


def random_city():
    """
    随机生成一个（中国）市
    """
    return fk.city()


def random_company():
    """
    生成一个随机的公司名称
    """
    return fk.company()


def random_postcode():
    """
    生成一个随机的邮政编码
    """
    return fk.postcode()


def random_email():
    """
    随机生成一个邮件地址
    """
    return fk.email()


def random_date():
    """
    返回一个随机的日期字符串
    """
    return fk.date()


def random_date_time():
    """
    返回一个随机的日期和时间字符串
    """
    return fk.date_time()


def random_natural():
    """
    返回一个随机的1-100的自然数（大于等于 0 的整数）
    """
    random_number = fk.random_int(min=1, max=100, step=1)
    return random_number


def random_float():
    """
    返回一个随机的浮点数，整数1-10，小数部分位数的最小值2，最大值5
    """
    random_number = round(fk.pyfloat(min_value=0, max_value=100), 2)
    return random_number


def random_character():
    """
    从字符串池返回随机的字符
    """
    character = fk.lexify()
    return character


def random_string():
    """
    从字符串池返回一个随机字符串，字符数1-10
    """
    string_pool = list(string.ascii_lowercase)
    ret_string = "".join(fk.random_sample(elements=string_pool, length=random.randint(1, 10)))
    return ret_string


def array_range(start, stop, step):
    """
    返回一个整型数组，参数分别：start：起始值，stop：结束值，step：步长
    """
    random_array = [fk.random_int(min=start, max=stop, step=step) for _ in range(stop // step)]
    return random_array


def guid():
    """
    随机生成一个 GUID
    """
    return fk.uuid4()


def url():
    """
    随机生成一个http URL
    """
    return fk.url()


def postcode():
    """
    生成一个随机的邮政编码
    """
    return fk.postcode()


def paragraph():
    """
    随机生成一段文本
    """
    return fk.text()


def title():
    """
    随机生成一个标题
    """
    return fk.sentence(nb_words=4)


def random_ipv4():
    """
    生成随机IPv4地址
    """
    return fk.ipv4()


def get_timestamp():
    """
    获取当前时间戳
    """
    return time.time()


def base64_encode(data: str):
    """
    用base64编码数据
    """
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def md5_encrypt(data: str):
    """
    使用MD5加密数据
    """
    from hashlib import md5
    new_md5 = md5()
    new_md5.update(data.encode('utf-8'))
    return new_md5.hexdigest()


def rsa_encrypt(msg, server_pub):
    """
    使用RSA加密加密消息
    """
    msg = msg.encode('utf-8')
    pub_key = server_pub.encode("utf-8")
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
    cryto_msg = rsa.encrypt(msg, public_key_obj)
    cipher_base64 = base64.b64encode(cryto_msg)
    return cipher_base64.decode()


def get_time_stamp(str_len=13):
    """
    获取具有指定长度的时间戳
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]

    raise exceptions.GetTimestampException("timestamp length can only between 0 and 16.")
