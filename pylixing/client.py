# -*- coding: utf-8 -*-
import hashlib
import logging

import requests

from . import templates, util
from .retry import retry_on_error
from .response import Response
from .models import (
    Location, UpdateInfo, SearchInfo,
    ProductDetail, GetSaleItemInfo, GetSaleItemDetail,
    Price, DailyPrices, ProductPickInfo,
    PricesCollection, Availability, BookLimit,
    Book, OrderStatus, Confirm, Refund, Date
)
from .exceptions import LixingException, LixingAPIError, ConnectionError

logger = logging.getLogger(__name__)


class LixingClient(object):
    """A simple client used to call Dida (http://www.didatravel.com/) APIs.

    :param user: user
    :param secret_key: secret_key used for signature
    :param url: API URL, default is http://api.lixing.biz/service
    :param timeout: seconds to wait for response
    :param raise_api_error: will raise :class:`~pylixing.exceptions.LixingAPIError`
                            if set to ``True`` when a request fails
    :param statsd_client: a StatsD client
    """

    def __init__(self, user, secret_key, url=None, timeout=20,
                 raise_api_error=True, statsd_client=None):
        self.user = user
        self.secret_key = secret_key
        self.url = url or 'http://api.lixing.biz/service'
        self.timeout = timeout
        self.raise_api_error = raise_api_error
        self.statsd_client = statsd_client

    def _timing(self, method, delta):
        if self.statsd_client and hasattr(self.statsd_client, 'timing'):
            return self.statsd_client.timing(method, delta)
        return util.fake_timing(method, delta)

    def get_location_info(self):
        """获取地理位置(国家/城市/区域)信息，可以获取每个地理位置在力行系统的编码。

        接口名称：getLocationInfo
        """
        return self._do_request('getLocationInfo', model_class=Location)

    def get_update_product_info(self, start_date, end_date='', start=1, end=10):
        """根据条件查询产品的code以及更新时间。该接口可以用来做产品信息和价格同步。

        接口名称：getUpdateProductInfo

        :param start_date: 最后更新时间起，string, 格式 '%Y-%m-%d'，如 '2015-10-11'
        :param end_date: 最后更新时间止，string, 格式同上，建议不填，默认当前日期
        :param start: 返回结果起始数，int, 最小为 1 (offset)
        :param end: 返回结果结束数，int, (offset+limit)
        """
        return self._do_request('getUpdateProductInfo',
                                start_date=start_date, end_date=end_date,
                                start=start, end=end,
                                model_class=UpdateInfo)

    def search_product(self, order_by='PRICE', start=1, end=10,
                       currency='CNY', ascend=True, destination_code='',
                       keyword='', product_codes=[], tags=[]):
        """根据条件查询产品的数量

        接口名称：根据条件查询产品的基本信息

        :param destination_code: 目的地code
        :param product_codes: 产品codes
        :param tags: 产品主题
        :param keyword: 关键字
        :param currency: 币种（CNY/HKD/USD）
        :param order_by: 按**排序（价格：PRICE，推荐:PRIORITY 默认为PRIORITY）
        :param ascend: 正序倒序(true/false)
        :param start: 返回结果起始数，最小为1
        :param end: 返回结果结束数（end与start之间差值需小于100）

        注意：
            不需要指定过多的条件

        """
        return self._do_request('searchProduct',
                                destination_code=destination_code,
                                product_codes=product_codes,
                                tags=tags, keyword=keyword,
                                currency=currency, order_by=order_by,
                                ascend=ascend, start=start, end=end,
                                model_class=SearchInfo)

    def search_product_count(self, destination_code='', product_codes=[],
                             tags=[], currency='CNY', keyword=''):
        """根据条件查询产品的数量

        接口名称：searchProductCount

        :param destination_code: 目的地code
        :param product_codes: 产品codes
        :param tags: 产品主题
        :param keyword: 关键字
        :param currency: 币种（CNY/HKD/USD）
        """
        return self._do_request('searchProductCount',
                                destination_code=destination_code,
                                product_codes=product_codes,
                                tags=tags, keyword=keyword,
                                currency=currency)

    def get_product_detail(self, product_code, currency='CNY'):
        """根据产品code查询产品详细信息

        接口名称：getProductDetail

        :param product_code: 产品 code
        :param currency: 币种
        """
        return self._do_request('getProductDetail',
                                product_code=product_code, currency=currency,
                                model_class=ProductDetail)

    def get_sale_item_info(self, product_code, currency='CNY'):
        """根据产品code查询产品详细信息

        接口名称：getProductDetail

        :param product_code: 产品 code
        :param currency: 币种
        """
        return self._do_request('getSaleItemInfo',
                                product_code=product_code, currency=currency,
                                model_class=GetSaleItemInfo)

    def get_sale_item_detail(self, sale_codes, currency='CNY'):
        """根据销售项目code查询销售项目的详细信息

        :param sale_codes: 销售项目code
        :param currency: 币种
        """
        return self._do_request('getSaleItemDetail',
                                sale_codes=sale_codes,
                                currency=currency,
                                model_class=GetSaleItemDetail)

    def get_price_by_day(self, sale_code, travel_date, currency='CNY'):
        """根据销售项目code和日期查询价格信息

        :param sale_code: 销售项目code
        :param travel_date: 日期
        :param currency: 币种
        """
        return self._do_request('getPriceByDay',
                                sale_code=sale_code,
                                travel_date=travel_date,
                                currency=currency,
                                model_class=Price)

    def get_price_by_period(self, sale_code, product_code,
                            travel_date, travel_date_end,
                            currency='CNY'):
        """根据销售项目code或者产品code和日期查询价格信息

        :param sale_code: 销售项目code
        :param product_code: 产品code
        :param travel_date: 旅行起始日期
        :param travel_date_end: 查询旅行终止日期
        :param currency: 币种
        """
        day_validated = util.validate_date(
            begin_date=travel_date,
            end_date=travel_date_end
        )
        if not day_validated:
            raise ValueError(u"旅行日期起（只能从前天开始）,最多只能查询31天价格")

        return self._do_request('getPriceByPeriod',
                                sale_code=sale_code,
                                product_code=product_code,
                                travel_date=travel_date,
                                travel_date_end=travel_date_end,
                                currency=currency,
                                model_class=DailyPrices)

    def get_available_dates(self, sale_code):
        """根据销售项目code查询可售日期信息

        :param sale_code: 销售项目code
        """
        return self._do_request('getAvailableDates',
                                sale_code=sale_code,
                                model_class=Date)

    def get_pick_or_drop(self, product_codes):
        """根据产品code查询接送信息

        :param product_codes: 产品code
        """
        return self._do_request('getPickOrDrop',
                                product_codes=product_codes,
                                model_class=ProductPickInfo)

    def get_price_segment(self, product_code, currency='CNY'):
        """与按天获取价格不同，返回一段时间内产品的价格（产品编码为S01起头的以及酒店产品不适用）

        :param product_code:
        :param currency:
        :return:
        """
        return self._do_request('getPriceSegment',
                                product_code=product_code,
                                currency=currency,
                                model_class=PricesCollection)

    def get_availability(self, sale_code, travel_date, end_date,
                         currency='CNY', booked_specifications=[],
                         booked_additional_options=[]):
        """传入购买的销售项目code，以及购买的规格或附加选项的code和数量，获取相应的可售信息和最新的准确价格信息

        :param sale_code: 销售项目code
        :param travel_date: 旅行起始时间
        :param end_date: 旅行终止时间
        :param currency: 币种
        :param booked_specifications: 购买规格
        :param booked_additional_options: 附加选项
        """
        return self._do_request('getAvailablity',  # 力行的拼写错误
                                sale_code=sale_code,
                                travel_date=travel_date,
                                end_date=end_date,
                                currency=currency,
                                booked_specifications=booked_specifications,
                                booked_additional_options=booked_additional_options,
                                model_class=Availability)

    def get_book_limits(self, sale_codes=[]):
        """传入saleCode获取预订限制

        :param sale_codes: 销售项目code列表
        """
        return self._do_request('getBookLimits',
                                sale_codes=sale_codes,
                                model_class=BookLimit)

    def book(self, distributor_order_refer, booker_name, booker_email,
             booker_phone, callback_url, items=[], currency='CNY'):
        """传入预订信息，创建订单，返回预订状态以及力行订单号

        :param distributor_order_refer: 分销商订单refers(必填)
        :param booker_name: 预订人姓名
        :param booker_email: 预订人邮箱(必填)
        :param booker_phone: 预订人手机(必填)
        :param callback_url: 出票回调，订单确认成功后，会回调这个地址，参数是order，value是力行的orderCd
        :param items:
            items=[
                {
                    "email": "bt@breadtrip.com",                                # 订项的email,收取确认邮件(必填)
                    "distributor_order_item_refer": "breadtriplixingorder001",  # 分销商订项号refer(必填)
                    # "pickup_code":                                            # 接的地点code，如果产品是支持接客人的，需要填写地点的code
                    # "pickup_point":                                           # 如果产品支持客人自己填写地址，客人自己写的接的地点
                    # "dropof_code":                                            # 送的地点code
                    # "dropoff_point":                                          # 客人自己写的送的地点
                    "travel_date": "2015-12-12",                                # 旅行时间（必填）
                    "product_code": "S01GB0520im30",                            # 产品code(必填)
                    "sale_code": "S011i082",                                    # 销售项目code(必填)
                    "special_requirements": u"力行",                             # 客人的特殊要求
                    # "book_questions": [],                                       # 客人填写的预订问题的答案，根据预订限制接口中是否有预订问题来决定是否需要此节点
                    "booked_specifications": [                                  # 预订的规格信息(必填)
                        {
                            "specification_id": "P1",
                            "num": 1,
                        }
                    ],
                    "leader": {                                                 # 领队人信息，根据预订限制接口来决定是否需要此节点
                        "phone": "+86 18718572345",                             # 领队人的联系电话
                        "crowd_type": "ADT",                                    # ADT/CHD/IFT(成人/儿童/婴儿)
                        "firstname": "bt",                                      # 名
                        "surname": "Gao",                                       # 姓
                        "gender": "Male",                                       # 性别MALE/FEMALE
                        "nationality_code": u"中国",                            # 国籍（中文名）
                        "birth": "1991-01-17",                                  # 出生年月日(1999-09-09)
                        "identity_type": "Identity Card",                       # 证件类型（从预订限制接口获取证件类型列表）
                        "identity_num": "440582199101178988",                   # 证件号码
                        "identity_expire_date": "2018-07-12",                   # 证件有效时间
                        "specifications": ["P1"],                               # 所属的规格（成人/儿童/青年）
                    },
                    # "travellers": [],                                         # 旅客信息，根据预订限制接口来决定是否需要此节点
                    # "booked_options": []                                      # 购买的附加选项
                    # "delivery":                                               # 配送根据预订限制接口来决定是否需要此节点
                }
            ]
        :param currency: 货币(必填)
        """
        return self._do_request('book',
                                distributor_order_refer=distributor_order_refer,
                                booker_name=booker_name,
                                booker_email=booker_email,
                                booker_phone=booker_phone,
                                callback_url=callback_url,
                                items=items,
                                currency=currency,
                                model_class=Book)

    def get_order_status(self, order_cds, ref_order_cds):
        """传入订单cd查询订单订项的状态

        :param order_cds: lixing订单cd
        :param order_cds: 分销商订单cd
        """
        return self._do_request('getOrderStatus',
                                order_cds=order_cds,
                                ref_order_cds=ref_order_cds,
                                model_class=OrderStatus)

    def confirm(self, order_cd):
        """传入需要确认的订单cd，力行会执行供应

        :param order_cd: 订单cd
        """
        return self._do_request('confirm',
                                order_cd=order_cd,
                                model_class=Confirm)

    def refund(self, order_cd, refund_reason, order_item_cd):
        """传入订单cd和 订项cd 进行整单退订

        :param order_cd: 订单cd
        :param refund_reason: 退订原因
        :param order_item_cd: 订项cd
        """
        return self._do_request('refund',
                                order_cd=order_cd,
                                order_item_cd=order_item_cd,
                                refund_reason=refund_reason,
                                model_class=Refund)

    @retry_on_error()
    def _do_request(self, method, **kwargs):
        model_class = kwargs.pop('model_class', None)
        body = util.join_lines(templates.render(method, **kwargs))
        data = {'user': self.user, 'sign': self.make_sign(body)}
        if body:
            data.update({'para': body})

        url = '%s?method=%s' % (self.url, method)

        # logger.info("%s %s", url, body)

        try:
            resp = self.session.post(url=url, data=data, timeout=self.timeout)
        except requests.ConnectionError as exc:
            logger.exception('pylixing catches ConnectionError')
            raise ConnectionError('ConnectionError: %s' % str(exc))
        except requests.RequestException as exc:
            logger.exception('pylixing catches RequestException')
            raise LixingException('RequestException: %s' % str(exc))
        except Exception as exc:
            logger.exception('pylixing catches unknown exception')
            raise LixingException('unknown exception: %s' % str(exc))

        logger.info('pylixing request: %s, %s', url, resp.request.body)
        # logger.info('pylixing response: %s', resp.content)

        rv = Response(resp)

        # save count_ps and timing to statsd
        self._timing("pylixing.%s" % method, rv.request_time)

        # logger.info("%s %s", url, body)
        # logger.info('pylixing response: %s', resp.content)
        # logger.info('pylixing elapsed: %sms', rv.request_time)

        if not rv.ok and self.raise_api_error:
            raise LixingAPIError(rv.api_code, rv.api_message)

        if model_class:
            rv.to_model(model_class)
        return rv

    @property
    def session(self):
        """A requests Session, which could make use of HTTP/1.1 Keep-Alive"""
        if not getattr(self, '_session', None):
            self._session = requests.Session()
        return self._session

    def make_sign(self, xml):
        """Calculate signature with given request xml data."""
        data = 'para%s%s' % (xml, self.secret_key) if xml else self.secret_key
        return hashlib.md5(data).hexdigest()
