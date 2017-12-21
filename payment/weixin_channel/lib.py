# -*- coding:utf-8 -*-

import random
import string
from bs4 import BeautifulSoup
from hashlib import md5
import requests
from payment.weixin_channel import config


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def nonceStr(length):
    """ 生成随机数"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def trans_dict_to_xml(data):
    """
    将字典转换成微信支付接口所需的xml格式数据
    :param data: dict
    :return xml
    """
    xml = []
    for k in sorted(data.keys()):
        v = data.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))


def trans_xml_to_dict(xml):
    """
    将微信支付接口返回的xml格式数据转化成字典
    :param xml: xml
    :return: dict
    """
    soup = BeautifulSoup(xml, features='xml')
    xml_data = soup.find('xml')
    if not xml_data:
        return {}
    result = dict([(item.name, item.text) for item in xml_data.find_all()])
    return result


def gen_sign(params, key):
    """
    签名生成函数
    :param params: 参数，dict对象
    :param key: API 密钥
    :return: sign string
    """
    param_list = []
    for k in sorted(params.keys()):
        v = params.get(k)
        if not str(v).strip():
            # 参数值为空的不参与签名
            continue
        param_list.append('{0}={1}'.format(k, v))
    param_list.append('key={}'.format(key))
    # 使用&连接'key=value'，并对字符串进行MD5加密
    return md5('&'.join(param_list).encode('utf-8')).hexdigest().upper()


def verify_sign(dict_res):
    """验证签名"""
    signature = dict_res.pop("sign", None)
    sign = gen_sign(params=dict_res, key=config.KEY)
    return sign == signature


def postXml(url, xml, second=30):
    """使用requests发送请求,不使用证书"""
    data = requests.post(url, data=xml, timeout=second)
    data.encoding = 'utf-8'
    return data.text



