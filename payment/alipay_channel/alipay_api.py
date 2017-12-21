# -*- coding:utf-8 -*-

from payment.alipay_channel import config
from payment.alipay_channel import lib

common_params = {
    "app_id": config.ALIPAY_APPID,
    "charset": config.CHARSET,
    "sign_type": config.SIGN_TYPE,
    "version": config.VERSION
}


def alipay_pay(order_id, total_amount, subject="标题", return_url=None, notify_url=None):
    """
    电脑网站支付
    :param order_id: 商户自定义订单号
    :param total_amount: 支付金额
    :param subject: 自定义订单标题
    :param return_url: 同步回调url
    :param notify_url: 异步回调url
    :return:
    """
    if not all([order_id, total_amount]):
        raise ValueError("missing parameter")
    if type(order_id) != str or type(total_amount) != str:
        raise TypeError("The type of the parameter must be a string")
    try:
        if float(total_amount) < 0.01:
            raise ValueError("支付金额最小单位为￥0.01")
    except Exception as e:
        raise TypeError("支付金额类型错误")
    
    biz_content = {
        "out_trade_no": order_id,
        "product_code": config.PRODUCT_CODE,
        "total_amount": total_amount,
        "subject": subject
    }
    # 组织请求参数
    data = lib.data_build(
        biz_content=biz_content,
        method=config.PAGE_PAY_NAME,
        common_params=common_params,
        return_url=return_url,
        notify_url=notify_url
    )
    # 对参数签名
    ordered_data = lib.sign_data(data)
    # 构造url
    url = lib.construct_url(ordered_data)
    return url


def alipay_query(out_trade_no=None, trade_no=None):
    """
    订单状态查询
    :param out_trade_no: 商户自定义订单号
    :param trade_no: 支付宝交易号
    :return:
    """
    if not any([out_trade_no, trade_no]):
        raise ValueError("missing parameter")
    biz_content = dict()
    if out_trade_no is not None:
        if type(out_trade_no) != str:
            raise TypeError("The type of the parameter must be a string")
        biz_content["out_trade_no"] = out_trade_no

    else:
        if type(trade_no) != str:
            raise TypeError("The type of the parameter must be a string")
        biz_content["trade_no"] = trade_no
    # 组织请求参数
    data = lib.data_build(
        biz_content=biz_content,
        method=config.ORDER_QUERY_NAME,
        common_params=common_params
    )
    # 对参数签名
    ordered_data = lib.sign_data(data)
    url = lib.construct_url(ordered_data)
    result = lib.get_response(url)
    # 对结果进行签名校验
    res = lib.verify_and_return_response(result, "alipay_trade_query_response")
    return res


def alipay_refund(order_id, refund_amount, refund_reason="正常退款", trade_no=None, out_request_no=None):
    """申请退款"""
    if any(value is None for value in (order_id, refund_amount)):
        raise ValueError("missing parameter")
    biz_content = {
        "out_trade_no": order_id,
        "refund_amount": refund_amount,
        "refund_reason": refund_reason,
        "trade_no": trade_no,
        "out_request_no": out_request_no
    }

    # 组织请求参数
    data = lib.data_build(
        biz_content=biz_content,
        method=config.REFUND_NAME,
        common_params=common_params
    )
    # 对参数签名
    ordered_data = lib.sign_data(data)
    # 构造url
    url = lib.construct_url(ordered_data)
    result = lib.get_response(url)
    # 校验结果
    res = lib.verify_and_return_response(result, "alipay_trade_refund_response")
    return res


def alipay_refund_query(order_id, out_request_no=None):
    """退款查询"""
    if order_id is None:
        raise ValueError("missing parameter")
    if out_request_no is None:
        out_request_no = order_id
    biz_content = {
        "out_trade_no": order_id,
        "out_request_no": out_request_no
    }
    # 组织请求参数
    data = lib.data_build(
        biz_content=biz_content,
        method=config.REFUND_QUERY_NAME,
        common_params=common_params
    )
    # 对参数签名
    ordered_data = lib.sign_data(data)
    # 构造url
    url = lib.construct_url(ordered_data)
    result = lib.get_response(url)
    # 校验结果
    res = lib.verify_and_return_response(result, "alipay_trade_fastpay_refund_query_response")
    return res



if __name__ == '__main__':
    order_id = '2017112415598569'
    total_amount = '0.01'
    subject = '测试订单008'
    print(alipay_pay(order_id, total_amount, subject))
    alipay_query(order_id)
