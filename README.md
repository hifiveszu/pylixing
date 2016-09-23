力行API Python SDK
==================

## 特性  
* 调用简单，根据参数生成请求 XML
* 支持(最新版本)[http://www.lixing.biz/home/doc/download?fileName=lixing_api_latest.pdf]所有 API
* 支持返回 XML 和 JSON 两种数据格式

## 安装

* 推荐使用 virtualenv (或 virtualenvwrapper)

```
pip install -e git+https://github.com/hifiveszu/pylixing.git@master#egg=pylixing
```

## 使用
```
>>> from pylixing import LixingClient
>>> lixing = LixingClient(user='***', secret_key='***',timeout=60)
>>> resp =  resp = lixing.get_order_status(order_cds=['160705T6554722'], ref_order_cds=[])
>>> resp.status_code
200
>>> resp.ok
True
>>> resp.data
[<OrderStatus: OrderStatus object>]
>>> order_status = resp.data
>>> order_status.to_primitive()
{'distributor_order_refer': u'***',
 'order_cd': u'***',
 'order_items': [{'distributor_order_item_refer': u'0',
   'order_item_cd': u'***',
   'refund_statuses': None,
   'remark': None,
   'status': u'10',
   'voucher_urls': [u'http://r.lixing.biz/***']}]}
```