# -*- coding:utf-8 -*-

import sys
from payment.alipay_channel import alipay_api


def test_alipay_pay():
    order_id = "2017112415598569"
    total_amount = "0.01"
    subject = "测试订单08"
    pay_url = alipay_api.alipay_pay(
        order_id=order_id,
        total_amount=total_amount,
        subject=subject
    )
    print(pay_url)


def test_alipay_query():
    order_id = "2017112415598569"
    res = alipay_api.alipay_query(out_trade_no=order_id)
    print(res)


def test_alipay_refund():
    order_id = "2017112415598569"
    refund_amount = "0.01"
    refund_reason = "无条件退款"
    res = alipay_api.alipay_refund(order_id=order_id, refund_amount=refund_amount, refund_reason=refund_reason)
    print(res)


def test_alipay_refund_query():
    order_id = "2017112415598569"
    res = alipay_api.alipay_refund_query(order_id=order_id)
    print(res)

if __name__ == '__main__':
    # test_alipay_pay()
    # test_alipay_query()
    # test_alipay_refund()
    test_alipay_refund_query()

