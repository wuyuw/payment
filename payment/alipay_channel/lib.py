# -*- coding:utf-8 -*-

import time
import json
from urllib import request, parse
import requests
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from base64 import encodebytes
from payment.alipay_channel import config


def get_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def data_build(biz_content, common_params, method, return_url=None, notify_url=None):
    """
    :param biz_content: dict
    :param common_params: dict
    :param method: 接口名
    :param return_url:
    :param notify_url:
    :return:
    """
    data = {
        "biz_content": biz_content,
        "timestamp": get_timestamp(),
        "method": method
    }
    data.update(common_params)
    if return_url is not None:
        data["return_url"] = return_url
    if method in (config.PAGE_PAY_NAME, config.WAP_PAY_NAME):
        if notify_url is not None:
            data["notify_url"] = notify_url
    return data


def ordered_data(data):
    """
    :param data: dict
    :return: 将value为dict的dumps成str
    """
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)
    for key in complex_keys:
        data[key] = json.dumps(data[key], separators=(',', ':'))
    return sorted([(k, v) for k, v in data.items()])


def generate_sign(data):
    """
    :param data: key1=val1&key2=val2...
    :return: signature
    """
    with open(config.APP_PRIVATE_KEY_PATH, 'r') as f:
        key = RSA.importKey(f.read())
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(data.encode('utf-8')))
    # base64编码
    sign = encodebytes(signature).decode('utf-8').replace('\n', '')
    return sign


def sign_data(data):
    """
    :param data: dict
    :return: get请求参数
    """
    data.pop('sign', None)
    # 将dict中value为dict的转为str
    unsigned_items = ordered_data(data)
    # 转换成key=value&key2=value2...
    unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
    # 生成签名
    sign = generate_sign(unsigned_string)
    ordered_items = ordered_data(data)
    # 拼接的时候将值使用parse.quote_plus()转化， 将 ' '和 + 替换掉
    ordered_string = "&".join("{}={}".format(k, parse.quote_plus(v)) for k, v in ordered_items)
    quoted_string = ordered_string + "&sign=" + parse.quote_plus(sign)
    return quoted_string


def construct_url(quoted_string):
    """构造url"""
    url = config.ALIPAY_URL + "?" + quoted_string
    return url


def get_response(url):
    """发送请求，获取响应"""
    response = request.urlopen(url=url, timeout=20)
    return response.read().decode('utf-8')


def func():
    def wrapper(url):
        response = request.urlopen(url=url, timeout=20)
        return response.read().decode('utf-8')
    return wrapper


def verify_and_return_response(raw_string, response_type):
    """
    校验签名并返回结果
    :param raw_string: response str
    :param response_type: str
    :return: dict or str
    """
    response = json.loads(raw_string)
    # 获取结果的有效部分
    result = response.get(response_type)
    # 获取签名
    sign = response.get("sign")
    # 获取待校验签名的字符串
    sign_string = get_sign_string(raw_string, response_type)
    if not sign_string:
        return "签名失败"
    # 校验签名
    if verify(sign_string, sign):
        return "签名失败"
    return result


def verify(sign_string, sign):
    with open(config.ALIPAY_PUBLIC_KEY_PATH, 'r') as fb:
        key = RSA.importKey(fb.read())
    signer = PKCS1_v1_5.new(key)
    digest = SHA256.new()
    digest.update(sign_string.encode('utf-8'))
    if signer.verify(digest, encodebytes(sign.encode('utf-8'))):
        return True
    return False


def get_sign_string(raw_string, response_type):
    """
    从返回的响应中提取待验签部分的字符串
    :param raw_string: 响应str
    :param response_type: 接口名称str
    :return: 待验签的str
    """
    index = raw_string.find(response_type)
    left_index = raw_string.find("{", index)
    right_index = raw_string.find("}", index)
    if -1 == left_index or -1 == right_index or left_index >= right_index:
        return None
    return raw_string[left_index: right_index + 1]


