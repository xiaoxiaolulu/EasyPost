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
    "postcode"
]


fk = Faker(locale='zh_CN')


def random_mobile():
    """随机生成手机号"""
    return fk.phone_number()


def random_name():
    """随机生成中文名字"""
    return fk.name()


def random_ssn():
    """随机生成一个省份证号"""
    return fk.ssn()


def random_addr():
    """随机生成一个地址"""
    return fk.address()


def random_city():
    """随机生成一个城市名"""
    return fk.city()


def random_company():
    """随机生成一个公司名"""
    return fk.company()


def random_postcode():
    """随机生成一个邮编"""
    return fk.postcode()


def random_email():
    """随机生成一个邮箱号"""
    return fk.email()


def random_date():
    """随机生成一个日期"""
    return fk.date()


def random_date_time():
    """随机生成一个时间"""
    return fk.date_time()


def random_natural():
    """返回一个随机的1-100的自然数（大于等于 0 的整数）"""
    random_number = fk.random_int(min=1, max=100, step=1)
    return random_number


def random_float():
    """生成一个范围在 0 到 100 之间的随机浮点数"""
    random_number = round(fk.pyfloat(min_value=0, max_value=100), 2)
    return random_number


def random_character():
    """返回随机的字符"""
    character = fk.lexify()
    return character


def random_string():
    """从字符串池返回一个随机字符串，字符数1-10"""
    string_pool = list(string.ascii_lowercase)
    ret_string = "".join(fk.random_sample(elements=string_pool, length=random.randint(1, 10)))
    return ret_string


def array_range(start, stop, step):
    """返回一个整型数组，参数分别：start：起始值，stop：结束值，step：步长"""
    random_array = [fk.random_int(min=start, max=stop, step=step) for _ in range(stop // step)]
    return random_array


def guid():
    """随机生成一个 GUID。例：eFD616Bd-e149-c98E-a041-5e12ED0C94Fd"""
    return fk.uuid4()


def url():
    """随机生成一个http URL"""
    return fk.url()


def postcode():
    """随机生成一个邮政编码"""
    return fk.postcode()


def random_ipv4():
    """随机生成一个ipv4的地址"""
    return fk.ipv4()


def get_timestamp():
    """生成当前时间戳"""
    return time.time()


def base64_encode(data: str):
    """base64编码"""
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def md5_encrypt(data: str):
    """md5加密"""
    from hashlib import md5
    new_md5 = md5()
    new_md5.update(data.encode('utf-8'))
    return new_md5.hexdigest()


def rsa_encrypt(msg, server_pub):
    """
    rsa加密
    :param msg: 待加密文本
    :param server_pub: 密钥
    :return:
    """
    msg = msg.encode('utf-8')
    pub_key = server_pub.encode("utf-8")
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
    cryto_msg = rsa.encrypt(msg, public_key_obj)  # noqa
    cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码
    return cipher_base64.decode()


if __name__ == '__main__':
    print(fk.postcode())
