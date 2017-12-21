# -*- coding:utf-8 -*-

from payment.weixin_channel import lib
from payment.weixin_channel import config


def unified_pay(body, out_trade_no, total_fee):
    """统一下单接口"""
    # 随机字符串
    nonce_str = lib.nonceStr(32)
    '''
    1.将有效参数转化为dict
    2.生成签名
    3.将参数转化成xml
    4.发送请求
    '''
    if any(value is None for value in (body, out_trade_no, total_fee)):
        raise ValueError("missing parameter")
    if int(float(total_fee)) < 1:
        return {"code": 0, "message": "金额必须为整型，最小值为1"}
    data = dict()
    data["appid"] = config.APPID
    data["mch_id"] = config.MCHID
    data["nonce_str"] = nonce_str
    data["trade_type"] = config.TRADE_TYPE
    data["out_trade_no"] = str(out_trade_no)  # 订单号
    data["body"] = str(body)  # 商品描述
    data["total_fee"] = int(total_fee)  # 支付金额(分)
    data["spbill_create_ip"] = config.IP  # ip
    data["notify_url"] = config.NOTIFY_URL  # 回调url
    # 生成签名
    data["sign"] = lib.gen_sign(data, key=config.KEY)
    # 转化成xml
    xml = lib.trans_dict_to_xml(data)
    # print(xml)
    try:
        # 发送请求
        response = lib.postXml(url=config.UNIFIED_ORDER_URL, xml=xml.encode('utf-8'))
    except Exception as e:
        print(e)
        return {"code": 0, "message": "请求下单失败"}
    # 将结果转化成dict
    dict_res = lib.trans_xml_to_dict(xml=response)
    if not lib.verify_sign(dict_res):
        return {"code": 0, "message": "签名校验失败"}
    if "SUCCESS" != dict_res.get("return_code", None):
        return {"code": 0, "message": dict_res.get("return_msg", "通讯失败")}
    if "SUCCESS" != dict_res.get("result_code", None):
        return {"code": 0, "message": dict_res.get("err_code_des", "订单生成失败")}
    result = {"prepay_id": dict_res.get("prepay_id", None), "code_url": dict_res.get("code_url", None)}
    return {"code": 1, "message": result}


def order_query(out_trade_no=None, transaction_id=None):
    """订单查询接口"""
    # 随机字符串
    nonce_str = lib.nonceStr(32)
    if out_trade_no is None and transaction_id is None:
        raise ValueError("missing parameter")
    data = dict()
    data["appid"] = config.APPID
    data["mch_id"] = config.MCHID
    data["nonce_str"] = nonce_str
    if out_trade_no is not None:
        data["out_trade_no"] = out_trade_no
    else:
        data["transaction_id"] = transaction_id
    # 生成签名
    data["sign"] = lib.gen_sign(data, key=config.KEY)
    # 转化成xml
    xml = lib.trans_dict_to_xml(data)
    try:
        # 发送请求
        response = lib.postXml(url=config.ORDER_QUERY_URL, xml=xml.encode('utf-8'))
    except Exception as e:
        return {"code": 0, "message": "查询失败"}
    # 将结果转化成dict
    dict_res = lib.trans_xml_to_dict(xml=response)
    if not lib.verify_sign(dict_res):
        return {"code": 0, "message": "signature error"}
    if "SUCCESS" != dict_res.get("return_code", None):
        return {"code": 0, "message": dict_res.get("return_msg", "通讯失败")}
    if "SUCCESS" != dict_res.get("result_code", None):
        return {"code": 0, "message": dict_res.get("err_code_des", "查询失败")}
    if "SUCCESS" != dict_res.get("trade_state"):
        result = {"trade_state": dict_res.get("trade_state", None), "trade_order_no": dict_res.get("trade_order_no", None)}
        return {"code": 1, "message": result}
    return {"code": 1, "message": dict_res}


def order_close(out_trade_no):
    """订单关闭接口"""
    if out_trade_no is None:
        raise ValueError("missing parameter")
    # 随机字符串
    nonce_str = lib.nonceStr(32)
    data = dict()
    data["appid"] = config.APPID
    data["mch_id"] = config.MCHID
    data["out_trade_no"] = out_trade_no
    data["nonce_str"] = nonce_str
    # 生成签名
    data["sign"] = lib.gen_sign(data, key=config.KEY)
    # 转化成xml
    xml = lib.trans_dict_to_xml(data)
    try:
        # 发送请求
        response = lib.postXml(url=config.ORDER_CLOSE_URL, xml=xml.encode('utf-8'))
    except Exception as e:
        return {"code": 0, "message": "请求失败"}
    # 将结果转化成dict
    dict_res = lib.trans_xml_to_dict(xml=response)
    if not lib.verify_sign(dict_res):
        return {"code": 0, "message": "signature error"}
    if "SUCCESS" != dict_res.get("return_code", None):
        return {"code": 0, "message": dict_res.get("return_msg", "通讯失败")}
    if "SUCCESS" != dict_res.get("result_code", None):
        return {"code": 0, "message": dict_res.get("err_code_des", None)}
    return {"code": 1, "message": "关闭订单成功"}


def resolve(xml):
    """处理回调通知的支付结果"""
    # 将结果转化成dict
    dict_res = lib.trans_xml_to_dict(xml=xml)
    if not lib.verify_sign(dict_res):
        return {"code": 0, "message": "signature error"}
    if "SUCCESS" != dict_res.get("return_code", None):
        return {"code": 0, "message": dict_res.get("return_msg", "通讯失败")}
    response = {"return_code": "SUCCESS"}
    response = lib.trans_dict_to_xml(response)
    if "SUCCESS" != dict_res.get("result_code", None):
        return {"code": 0, "message": dict_res.get("err_code_des", "交易失败"), "response": response}
    return {"code": 1, "message": dict_res, "response": response}


def refund(out_trade_no, out_refund_no, total_fee, refund_fee, transaction_id=None):
    """申请退款接口"""
    if transaction_id is None and any(value is None for value in (out_trade_no, out_refund_no, total_fee, refund_fee)):
        raise ValueError("missing parameter")
    if transaction_id is not None and any(value is None for value in (out_refund_no, total_fee, refund_fee)):
        raise ValueError("missing parameter")
    # 随机字符串
    nonce_str = lib.nonceStr(32)
    data = dict()
    data["appid"] = config.APPID
    data["mch_id"] = config.MCHID
    data["out_trade_no"] = out_trade_no
    data["nonce_str"] = nonce_str
    data["transaction_id"] = transaction_id
    data["out_refund_no"] = out_refund_no
    data["total_fee"] = total_fee
    data["refund_fee"] = refund_fee
    # 生成签名
    data["sign"] = lib.gen_sign(data, key=config.KEY)
    # 转化成xml
    xml = lib.trans_dict_to_xml(data)
    try:
        # 发送请求
        response = lib.postXml(url=config.REFUND_URL, xml=xml.encode('utf-8'))
    except Exception as e:
        print(e)
        return {"code": 0, "message": "请求失败"}
    # 将结果转化成dict
    dict_res = lib.trans_xml_to_dict(xml=response)
    if not lib.verify_sign(dict_res):
        return {"code": 0, "message": "signature error"}
    if "SUCCESS" != dict_res.get("return_code", None):
        return {"code": 0, "message": dict_res.get("return_msg", "通讯失败")}
    if "SUCCESS" != dict_res.get("result_code", None):
        return {"code": 0, "message": dict_res.get("err_code_des", None)}
    return {"code": 1, "message": dict_res}


def refund_query(transaction_id=None, out_trade_no=None, out_refund_no=None, refund_id=None):
    """退款查询接口"""
    if all(value is None for value in (transaction_id, out_trade_no, out_refund_no, refund_id)):
        raise ValueError("missing parameter")
    # 随机字符串
    nonce_str = lib.nonceStr(32)
    data = dict()
    data["appid"] = config.APPID
    data["mch_id"] = config.MCHID
    data["out_trade_no"] = out_trade_no
    data["nonce_str"] = nonce_str
    data["transaction_id"] = transaction_id
    data["out_refund_no"] = out_refund_no
    data["refund_id"] = refund_id
    # 生成签名
    data["sign"] = lib.gen_sign(data, key=config.KEY)
    # 转化成xml
    xml = lib.trans_dict_to_xml(data)
    try:
        # 发送请求
        response = lib.postXml(url=config.REFUND_QUERY_URL, xml=xml)
    except Exception as e:
        return {"code": 0, "message": "请求失败"}
    # 将结果转化成dict
    dict_res = lib.trans_xml_to_dict(xml=response)
    if not lib.verify_sign(dict_res):
        return {"code": 0, "message": "signature error"}
    if "SUCCESS" != dict_res.get("return_code", None):
        return {"code": 0, "message": dict_res.get("return_msg", "通讯失败")}
    if "SUCCESS" != dict_res.get("result_code", None):
        return {"code": 0, "message": dict_res.get("err_code_des", None)}
    return {"code": 1, "message": dict_res}

