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

## API 和 LixingClient 的方法对应表

API | 方法名 | 说明
----|----|----
getLocationInfo | get\_location\_info | 获取地理位置
getUpdateProductInfo | get\_update\_product\_info | 根据条件查询产品的code以及更新时间。该接口可以用来做产品信息和价格同步。
searchProduct | search\_product | 根据条件查询产品的基本信息
searchProductCount | search\_product\_count | 根据条件查询产品的数量
getProductDetail | get\_product\_detail | 根据产品code查询产品详细信息
getSaleItemInfo | get\_sale\_item\_info | 根据产品code查询产品详细信息
getSaleItemDetail | get\_sale\_item_detail | 根据销售项目code查询销售项目的详细信息
getPriceByDay | get\_price\_by\_day | 根据销售项目code和日期查询价格信息
getPriceByPeriod | get\_price\_by\_period | 根据销售项目code或者产品code和日期查询价格信息
getAvailableDates | get\_available\_dates | 根据销售项目code查询可售日期信息
getPickOrDrop | get\_pick\_or\_drop | 根据产品code查询接送信息
getPriceSegment | get\_price\_segment | 与按天获取价格不同，返回一段时间内产品的价格（产品编码为S01起头的以及酒店产品不适用）
getAvailablity | get\_availability | 传入购买的销售项目code，以及购买的规格或附加选项的code和数量，获取相应的可售信息和最新的准确价格信息。注意:'getAvailablity',为力行的拼写错误
getBookLimits | get\_book\_limits | 传入saleCode获取预订限制
book | book | 传入预订信息，创建订单，返回预订状态以及力行订单号
getOrderStatus | get\_order\_status | 传入订单cd查询订单订项的状态confirm | confirm | 传入需要确认的订单cd，力行会执行供应
refund | refund | 传入订单cd和 订项cd 进行整单退订

## 文档

- 力行 API 文档：[lixing\_api\_latest.pdf](docs/lixing_api_latest.pdf)

## 联系作者

欢迎使用并改进，有任何问题请联系：<hifiveszu@gmail.com>