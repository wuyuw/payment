# -*- coding:utf-8 -*-

import os

# alipay沙箱应用APPID
# ALIPAY_APPID = ''
#  应用2.0
ALIPAY_APPID = ''

# payment的绝对路径
BASI_DIR = os.path.dirname(os.path.realpath(__file__))
# 请求url
ALIPAY_URL = 'https://openapi.alipay.com/gateway.do'
# 接口名称
PAGE_PAY_NAME = 'alipay.trade.page.pay'  # 电脑网站支付
WAP_PAY_NAME = 'alipay.trade.wap.pay'  # 手机网站支付
ORDER_QUERY_NAME = 'alipay.trade.query'  # 订单查询
REFUND_NAME = 'alipay.trade.refund'  # 退款
REFUND_QUERY_NAME = 'alipay.trade.fastpay.refund.query'  # 退款查询


# 请求编码格式
CHARSET = 'utf-8'
# 签名算法类型
SIGN_TYPE = 'RSA2'
# 接口版本
VERSION = '1.0'

# 销售产品码
PRODUCT_CODE = 'FAST_INSTANT_TRADE_PAY'

# app密钥路径
APP_PRIVATE_KEY_PATH = os.path.join(BASI_DIR, 'app_private_key.pem')
# alipay公钥路径
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASI_DIR, 'alipay_public_key.pem')


