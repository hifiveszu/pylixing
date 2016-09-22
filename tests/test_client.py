# -*- coding: utf-8 -*-
import os
import sys
import logging

sys.path.insert(0, os.path.abspath('..'))

from pylixing.client import LixingClient


def init_logger():
    logger = logging.getLogger('pylixing')
    handler = logging.StreamHandler()
    fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    handler.setFormatter(logging.Formatter(fmt))
    handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


init_logger()

lixing = LixingClient(user='****',
                      secret_key='****',
                      timeout=60)


def test_get_location_info():
    resp = lixing.get_location_info()
    locations = resp.data
    for location in locations:
        print location.to_primitive()
    print len(locations)


def test_get_update_product_info():
    resp = lixing.get_update_product_info(start_date='2000-11-11', start=1, end=10)
    for info in resp.data:
        print info.to_primitive()
    print len(resp.data)


def test_get_product_detail():
    resp = lixing.get_product_detail(
        # product_code='',
        # product_code='D53GA09I00030',
        # product_code='S01GB0520im30',
        product_code='S01US01K1ib72'
    )
    detail = resp.data
    if detail:
        print detail.to_primitive().keys()


def test_search_product():
    resp = lixing.search_product(
        # destination_code='TH',
        destination_code='',
        # product_codes=['D53GA09I00030'],
        product_codes=[],
        # product_codes=[],
        # tags=['T033'],
        tags=[],
        keyword=u'泰国',
        # keyword=u'',
        currency='CNY',
        # order_by='PRICE',
        order_by='',
        # ascend='true',
        ascend='',
        start=1,
        end=2,
    )
    for info in resp.data:
        print info.to_primitive()


def test_search_product_count():
    resp = lixing.search_product_count(
        # destination_code='TH',
        destination_code='',
        # product_codes=['D53GA09I00030'],
        product_codes=[],
        tags=[],
        # keyword=u'人妖',
        keyword='',
        currency='CNY',
    )
    result = resp.data
    print result['count']


def test_get_sale_item_info():
    # resp = lixing.get_sale_item_info(product_code='S01US01T23b28', currency='CNY')
    # codes = [
    #     'D3lTH0DC01n73', 'D60JP0AC00b98', 'D1pSG0CN01v91', 'D53GA09I00030'
    # ]
    # codes = ['S01US01K1ib72']
    # codes = ['S01US01719r20']
    # codes = ['S01ES04S0b211']
    # codes = ['S01MX0B374469']   # 拼车接机：瓜达拉哈拉机场至市区酒店
    # codes = ['S01US00J1g321'] # 往返接送：阿纳海姆/布埃纳公园市区酒店至好莱坞环球影城
    # codes = ['S01IT04212337'] # 托斯卡纳葡萄酒品酒小团游
    # codes = ['S01US00P1px05'] # 购物接送
    codes = ['S01US01J2sf86'] # 购物游
    for code in codes:
        resp = lixing.get_sale_item_info(
            product_code=code,
            currency='CNY'
        )
        item_info = resp.data
        data = item_info.to_primitive()
        print data
        for e in data['sale_item_infos']:
            print e['sale_code']
        # print item_info.to_primitive()


def test_get_sale_item_detail():
    sale_codes = ['D3l06o40']

    resp = lixing.get_sale_item_detail(sale_codes=sale_codes)
    sale_detail = resp.data
    print sale_detail.to_primitive()


def test_get_price_by_day():
    resp = lixing.get_price_by_day(
        sale_code='D1p02i432',
        travel_date="2015-12-11",
        currency="CNY",
    )
    prices = resp.data or []
    for e in prices:
        print e.to_primitive()


def test_get_price_by_period():
    resp = lixing.get_price_by_period(
        sale_code='D1p02i432',
        product_code="",
        travel_date="2016-04-23",
        travel_date_end="2016-05-10",
        currency="CNY",
    )
    prices = resp.data
    for e in prices:
        print e.to_primitive()


def test_get_available_dates():
    resp = lixing.get_available_dates(
        sale_code='D1p02i432',
    )
    data = resp.data
    print data


def test_get_pick_or_drop():
    resp = lixing.get_pick_or_drop(product_codes=["S01US01915y25"])
    infos = resp.data
    for info in infos:
        print info.to_primitive()


def test_get_price_segment():
    resp = lixing.get_price_segment(product_code="D3rCN09D00297", currency='CNY')
    price_segment = resp.data
    for seg in price_segment.price_segments:
        print seg.to_primitive()


def test_get_availability():
    resp = lixing.get_availability(
        sale_code="D1p02i432",
        currency='CNY',
        travel_date='2015-12-12',
        end_date='2015-12-22',
        booked_specifications=[],
        booked_additional_options=[],
    )
    availability = resp.data
    print availability.to_primitive()


def test_get_book_limits():
    # sale_codes = ['S018qi541', 'S018qj551']
    # sale_codes = ['S0195g393', 'S0195h394']
    # sale_codes = ['S011i082']
    # sale_codes = ['S010sc42', "S010sd43", "S010se44", "S010sf45"]
    # sale_codes = ['S01khd911']
    # sale_codes = ['S018jt581'] # 往返接送：阿纳海姆/布埃纳公园市区酒店至好莱坞环球影城
    # sale_codes = ['S017vt69'] # 美食游
    # sale_codes = ['S019dh411'] # 购物接送
    sale_codes = ['S01cbg801']  # 购物游
    resp = lixing.get_book_limits(sale_codes=sale_codes)
    book_limits = resp.data
    for limit in book_limits:
        rest = limit.to_primitive()
        print rest
        # quest = rest['questions'] if 'questions' in rest else []
        # for e in quest:
        #     print e['content'], e['code'], e['required']


def test_book():
    data = dict(
        distributor_order_refer="breadtriplixingorder001",
        currency='CNY',
        booker_name=u'Kitto Zheng',
        booker_email=u'zhengzhijie@breadtrip.com',
        booker_phone=u'18718572432',
        callback_url='',
        items=[
            {
                "email": "zhengzhijie@breadtrip.com",
                "distributor_order_item_refer": "breadtriplixingorder001",
                "travel_date": "2015-12-24",
                "product_code": "S01GB0520im30",
                "sale_code": "S011i082",
                "special_requirements": u"力行",
                "booked_specifications": [
                    {
                        "specification_id": "P1",
                        "num": 1,
                    }
                ],
                "leader": {
                    "phone": "+86 18718572345",
                    "crowd_type": "ADT",
                    "firstname": "Kitto",
                    "surname": "Zheng",
                    "gender": "Male",
                    "nationality_code": u"中国",
                    "birth": "1991-01-17",
                    "identity_type": "Identity Card",
                    "identity_num": "440582199101178988",
                    "identity_expire_date": "2018-07-12",
                    "specifications": ["P1"],
                }
            },
            # {
            #     "email": "zhengzhijie@breadtrip.com",
            #     "distributor_order_item_refer": "breadtriplixingorder001",
            #     "travel_date": "2015-12-24",
            #     "product_code": "S01MX0B374469",
            #     "sale_code": "S01khd911",
            #     "special_requirements": u"力行",
            #     "booked_specifications": [
            #         {
            #             "specification_id": "P1",
            #             "num": 1,
            #         }
            #     ],
            #     "leader": {
            #         "phone": "+86 18718572345",
            #         "crowd_type": "ADT",
            #         "firstname": "Kitto",
            #         "surname": "Zheng",
            #         "gender": "Male",
            #         "nationality_code": u"中国",
            #         "birth": "1991-01-17",
            #         "identity_type": "Identity Card",
            #         "identity_num": "440582199101178988",
            #         "identity_expire_date": "2018-07-12",
            #         "specifications": ["P1"],
            #     },
            #     "book_questions" : [
            #         {
            #             "question_id": 7,
            #             "answer": "United xx",
            #         },
            #         {
            #             "question_id": 8,
            #             "answer": "UA 864",
            #         },
            #         {
            #             "question_id": 12,
            #             "answer": "8pm"
            #         },
            #         {
            #             "question_id": 11,
            #             "answer": "holly shit"
            #         }
            #
            #     ]
            # }
        ],

    )
    resp = lixing.book(**data)
    book = resp.data
    print book.to_primitive()


def test_get_order_status():
    resp = lixing.get_order_status(order_cds=['151130T3821128'], ref_order_cds=['160918T7966358'])
    order_statuses = resp.data
    for order_status in order_statuses:
        print order_status.to_primitive()


def test_confirm():
    resp = lixing.confirm(order_cd='151130T3821128')
    confirm = resp.data
    if confirm:
        print confirm.to_primitive()


def test_refund():
    resp = lixing.refund(
        order_cd='151130T3821128',
        order_item_cd='151130T3821128001',
        refund_reason=u'订单信息有误'
    )
    refund = resp.data
    if refund:
        print refund.to_primitive()


if __name__ == "__main__":
    test_get_location_info()
    test_get_update_product_info()
    test_get_product_detail()
    test_search_product()
    test_search_product_count()
    test_get_sale_item_info()
    test_get_sale_item_detail()
    test_get_price_by_day()
    test_get_price_by_period()
    test_get_available_dates()
    test_get_pick_or_drop()
    test_get_price_segment()
    test_get_availability()
    test_get_book_limits()
    test_book()
    test_get_order_status()
    test_confirm()
    test_refund()

    # 1. test_get_sale_item_info (product_code)
    # 2. test_get_book_limits (sale_code)
