import base64
import time
import rsa
from faker import Faker

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


def radom_date_time():
    """随机生成一个时间"""
    return fk.date_time()


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
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)  #
    cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
    cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码
    return cipher_base64.decode()
