# -*- coding:utf-8 -*-

import sys
from payment.weixin_channel import weixin_pay


def test_weixin_pay():
    out_trade_no = "201712041747"
    total_fee = "1"
    body = "测试订单018"
    res = weixin_pay.unified_pay(out_trade_no=out_trade_no, total_fee=total_fee, body=body)
    print(res)


def test_order_query():
    out_trade_no = "201712041747"
    res = weixin_pay.order_query(out_trade_no=out_trade_no)
    print(res)


def test_order_close():
    out_trade_no = "201712041747"
    res = weixin_pay.order_close(out_trade_no=out_trade_no)
    print(res)


if __name__ == '__main__':
    # test_weixin_pay()
    # test_order_query()
    test_order_close()
