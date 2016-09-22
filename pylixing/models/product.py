# -*- coding: utf-8 -*-
from schematics.models import Model
from schematics.types import StringType, URLType, BooleanType, IntType
from schematics.types.compound import ListType, ModelType

from ..util import ensure_list


class UpdateInfo(Model):
    product_code = StringType()
    product_name = StringType()
    last_update_time = StringType()
    last_update_action = StringType()  # RELEASE上架/OFF_SHELF下架/UPDATE更新

    @classmethod
    def new_from_info(cls, info):
        """把 <product-code-info></product-code-info> 节点转换成 UpdateInfo 类型

        :param info: dict or ordereddict
        """
        rv = cls()
        for k, v in info.iteritems():
            # API 返回的 XML 节点用 '-' 连接，这里换成 '_'
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        """把 <product-code-infos></product-code-infos> 转换成 [UpdateInfo] 类型
        :param data: dict 类型
        """
        if not data:
            return []
        infos_node = data['product-code-infos']
        infos = ensure_list(infos_node.get('product-code-info', []))
        return [cls.new_from_info(info) for info in infos]


class SearchCount(Model):
    count = IntType()

    @classmethod
    def new_from_api(cls, data):
        """把 <count></count> 转换成 [SearchCount] 类型
        :param data: dict 类型
        """
        infos_node = data['count']
        infos = ensure_list(infos_node.get('count', []))
        return [cls.new_from_info(info) for info in infos]


class SearchInfo(Model):
    product_code = StringType()  # 产品code
    product_name = StringType()  # 产品名称
    currency = StringType()  # 币种（CNY/HKD/USD）
    category = StringType()  # 主分类codes
    sub_category = StringType()  # 二级分类code
    duration_type = StringType()  # 时长类型（DURATION_DAYS几天几晚/DURATION_HOURS表示几小时几分钟）
    duration_part1 = StringType()  # 天数/小时数(由DurationType定)
    duration_part2 = StringType()  # 晚数/分钟数(由DurationType定)
    short_desc = StringType()  # 简要描述
    main_pic = StringType()  # 主图地址
    recommend_level = StringType()  # 推荐等级
    net_price_from = StringType()  # 净价起
    retail_price_from = StringType()  # 市场价起
    location = StringType()  # 地址（例如：美国 纽约）
    destination_code = StringType()  # 目的地code
    district_code = StringType()  # 所在行政区code
    city_code = StringType()  # 所在城市code
    region_code = StringType()  # 所在地区code
    country_code = StringType()  # 所在国家code
    tags = StringType()  # 主题 code
    star_level = StringType()  # 星级
    product_type = StringType()  # 产品类型

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not data:
            return []

        info_nodes = data['product-list']
        infos = ensure_list(info_nodes.get('product-info', []))
        return [cls.new_from_info(info) for info in infos]


class ProductDescription(Model):
    title = StringType()  # 标题
    content = StringType()  # 内容
    image = URLType()  # 图片

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'descriptions' in data):
            return []

        info_nodes = data['descriptions']
        infos = ensure_list(info_nodes.get('description', []))
        return [cls.new_from_info(info) for info in infos]


class IncludeCrowd(Model):
    crowd_type = StringType()  # 人群类型(ADT成人/CHD儿童/IFT婴儿/SNR老年/YTH青年)
    crowd_name = StringType()  # 人群名称
    age_from = StringType()  # 年龄起
    age_to = StringType()  # 年龄止
    min_num = StringType()  # 单一人群最少出行人数
    max_num = StringType()  # 单一人群最多出行人数

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'include_crowds' in data):
            return []

        infos = ensure_list(data['include_crowds'])
        return [cls.new_from_info(info) for info in infos]


class ProductSpecification(Model):
    specification_id = StringType()  # 规格id
    specification_type = StringType()  # 规格类型（PERSON人群，BED床型，ITEM旅游项目）
    crowd_type = StringType()  # 人群类型(ADT成人/CHD儿童/IFT婴儿/SNR老年/YTH青年)
    description = StringType()  # 英文描述
    description_cn = StringType()  # 中文描述
    age_from = StringType()  # 年龄起
    age_to = StringType()  # 年龄止
    team_leader = BooleanType()  # 是否可以作为领队人
    bed_size = StringType()  # 床型尺寸（酒店专用）
    include_crowds = ListType(ModelType(IncludeCrowd))  # 组合规格（如2成人1儿童家庭套餐）

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == 'team_leader':
                new_v = v == 'true'
            if the_key == "include_crowds":
                new_v = IncludeCrowd.new_from_api(data={'include_crowds': v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'product_specifications' in data):
            return []

        info_nodes = data['product_specifications']
        infos = ensure_list(info_nodes.get('product-specification', []))
        return [cls.new_from_info(info) for info in infos]


class Photo(Model):
    title = StringType()  # 照片标题
    caption = StringType()  # 描述
    url = StringType()  # 图片地址

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'photos' in data):
            return []

        info_nodes = data['photos']
        infos = ensure_list(info_nodes.get('product-photo', []))
        return [cls.new_from_info(info) for info in infos]


class BookQuestion(Model):
    question_id = StringType()  # 问题id，预订的时候传
    content = StringType()  # 内容
    required = BooleanType()  # 是否必须回答
    example = StringType()  # 回答示例

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            if the_key == 'required':
                v = v == 'true'
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'book_questions' in data):
            return []

        info_nodes = data['book_questions']
        infos = ensure_list(info_nodes.get('book－question', []))
        return [cls.new_from_info(info) for info in infos]


class ExtendProperty(Model):
    code = StringType()  # 属性code
    name = StringType()  # 属性name
    value = StringType()  # 属性值

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'extend_properties' in data):
            return []

        info_nodes = data['extend_properties']
        infos = ensure_list(info_nodes.get('extend-property', []))
        return [cls.new_from_info(info) for info in infos]


class ProductPhoto(Model):
    title = StringType()  # 照片标题
    url = StringType()  # 照片地址

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'product_photos' in data):
            return []

        info_nodes = data['product_photos']
        infos = ensure_list(info_nodes.get('product-photo', []))
        return [cls.new_from_info(info) for info in infos]


class ItineraryTraffic(Model):
    departure = StringType()  # 出发信息
    arrival = StringType()  # 到达信息
    traffic_info = StringType()  # 交通信息

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'itinerary_traffic' in data):
            return None
        return cls.new_from_info(data['itinerary_traffic'])


class ItineraryHotel(Model):
    hotel_name = StringType()  # 酒店名
    hotel_level = StringType()  # 酒店星级
    hotel_photos = ListType(ModelType(ProductPhoto))  # 酒店照片
    hotel_address = StringType()  # 酒店地址
    district = StringType()  # 酒店所在区域
    room_bed_name = StringType()  # 床型信息
    hotel_description = StringType()  # 酒店描述
    book_note = StringType()  # 酒店预订须知

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "hotel_photos":
                new_v = ProductPhoto.new_from_api(data={'product_photos': v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'hotels' in data):
            return []

        info_nodes = data['hotels']
        infos = ensure_list(info_nodes.get('itinerary-hotel', []))
        return [cls.new_from_info(info) for info in infos]


class Itinerary(Model):
    itinerary_title = StringType()  # 行程描述
    routes = ListType(StringType())  # 行程途径地
    breakfast_type = StringType()  # 早餐类型（中文描述）
    breakfast_description = StringType()  # 早餐描述
    lunch_type = StringType()  # 午餐类型（中文描述）
    lunch_description = StringType()  # 午餐描述
    dinner_type = StringType()  # 晚餐类型（中文描述）
    dinner_description = StringType()  # 晚餐描述
    itinerary_photos = ListType(ModelType(ProductPhoto))  # 行程照片
    itinerary_traffic = ModelType(ItineraryTraffic)  # 交通信息
    hotels = ListType(ModelType(ItineraryHotel))  # 酒店信息
    itinerary_introduce = StringType()  # 行程介绍
    attractions = ListType(StringType())  # 途径的景点

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "itinerary_photos":
                new_v = ProductPhoto.new_from_api(data={'product_photos': v})
            if the_key == "itinerary_traffic":
                new_v = ItineraryTraffic.new_from_api(
                    data={'itinerary_traffic': v})
            if the_key == "hotels":
                new_v = ItineraryHotel.new_from_api(data={'hotels': v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'itineraries' in data):
            return []

        info_nodes = data['itineraries']
        infos = ensure_list(info_nodes.get('itinerary', []))
        return [cls.new_from_info(info) for info in infos]


class SalePoint(Model):
    sale_point = StringType()  # 卖点

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'sale_points' in data):
            return []

        info_nodes = data['sale_points']
        infos = ensure_list(info_nodes.get('sale_point', []))
        return [cls.new_from_info(info) for info in infos]


class ProductDetail(Model):
    product_code = StringType()  # 产品code
    product_name = StringType()  # 产品名称
    product_type = StringType()  # 产品类型
    currency = StringType()  # 币种（CNY/HKD/USD）
    category = StringType()  # 主分类code
    sub_category = StringType()  # 二级分类code
    duration_type = StringType()  # 时长类型（DURATION_DAYS几天几晚/DURATION_HOURS表示几小时几分钟）
    duration_part1 = StringType()  # 天数/小时数(由DurationType定)
    duration_part2 = StringType()  # 晚数/分钟数(由DurationType定)
    short_description = StringType()  # 简要描述
    main_pic = StringType()  # 主图地址
    recommend_level = StringType()  # 推荐等级
    location = StringType()  # 地址（例如：美国 纽约）
    dest_code = StringType()  # 目的地code
    district_code = StringType()  # 所在行政区code
    city_code = StringType()  # 所在城市code
    region_code = StringType()  # 所在地区code
    country_code = StringType()  # 所在国家code
    continent_code = StringType()  # 所在大洲code
    tags = StringType()  # 主题分类
    star_level = StringType()  # 星级（酒店专用）
    lat = StringType()  # 纬度
    lon = StringType()  # 经度
    dest_name = StringType()  # 目的地名称
    depart_name = StringType()  # 出发地名称
    depart_code = StringType()  # 出发地code
    descriptions = ListType(ModelType(ProductDescription))  # 详细介绍 多个
    departure_time = StringType()  # 出发时间
    departure_point = StringType()  # 出发地点
    departure_remark = StringType()  # 出发备注
    drop_off_time = StringType()  # 解散时间
    drop_off_point = StringType()  # 解散地点
    drop_off_remark = StringType()  # 解散备注
    pick_up = StringType()  # 是否接
    pickup_on_request = BooleanType()  # 是否可以由客人自填接人地址
    drop_off = BooleanType()  # 是否送
    drop_off_on_request = BooleanType()  # 是否可以由客人自填送人地址
    sale_points = ListType(ModelType(SalePoint))  # 卖点
    net_price_from = StringType()  # 净价起
    net_price_from_desc = StringType()  # 起价说明
    retail_price_from = StringType()  # 市场价起
    inclusions = StringType()  # 费用包含
    exclusions = StringType()  # 费用不包含
    address = StringType()  # 地址
    tel = StringType()  # 电话
    website = StringType()  # 网址
    hotel_star = StringType()  # 酒店星级
    opening_hours = StringType()  # 营业时间
    attentions = StringType()  # 注意事项
    product_specifications = ListType(ModelType(ProductSpecification))  # 规格类型
    photos = ListType(ModelType(Photo))  # 照片
    book_questions = ListType(ModelType(BookQuestion))  # 预订需要填写的问题例如飞机航班号
    extend_properties = ListType(ModelType(ExtendProperty))  # 扩展字段
    itineraries = ListType(ModelType(Itinerary))  # 多日行程描述，category为目的地参团和出发地参团的产品有此内容

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "descriptions":
                new_v = ProductDescription.new_from_api(data={'descriptions': v})
            if the_key == "sale_points":
                new_v = SalePoint.new_from_api(data={'sale_points': v})
            if the_key == "product_specifications":
                new_v = ProductSpecification.new_from_api(data={'product_specifications': v})
            if the_key == "photos":
                new_v = Photo.new_from_api(data={'photos': v})
            if the_key == "book_questions":
                new_v = BookQuestion.new_from_api(data={'book_questions': v})
            if the_key == "extend_properties":
                new_v = ExtendProperty.new_from_api(data={'extend_properties': v})
            if the_key == "itineraries":
                new_v = Itinerary.new_from_api(data={'itineraries': v})
            if the_key in ['pickup_on_request', 'drop_off', 'drop_off_on_request']:
                new_v = v == 'true'
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'product-detail' in data):
            return []

        info_node = data['product-detail']
        return cls.new_from_info(info_node)


class SaleItemInfo(Model):
    sale_code = StringType()  # 销售项目code
    sale_name = StringType()  # 销售项目名称
    desc = StringType()  # 描述
    net_price_from = StringType()  # 净价起
    retail_price_from = StringType()  # 市场价起

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'sale-item-infos' in data):
            return []

        infos_node = data['sale-item-infos']
        infos = ensure_list(infos_node.get('sale-item-info', []))
        return [cls.new_from_info(info) for info in infos]


class GetSaleItemInfo(Model):
    sale_item_infos = ListType(ModelType(SaleItemInfo))  # 可重复节点
    product_specifications = ListType(ModelType(ProductSpecification))  # 同产品详情接口

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == 'sale_item_infos':
                new_v = SaleItemInfo.new_from_api(data={"sale-item-infos": v})
            if the_key == 'product_specifications':
                new_v = ProductSpecification.new_from_api(data={"product_specifications": v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not data:
            return None

        return cls.new_from_info(data)


class AddressDetail(Model):
    time = StringType()  # 取票时间
    point = StringType()  # 取票地点
    address = StringType()  # 取票详细地址

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'address_details' in data):
            return []

        infos_node = data['address_details']
        infos = ensure_list(infos_node.get('address-detail', []))
        return [cls.new_from_info(info) for info in infos]


class VoucherInfo(Model):
    need_delivery = StringType()  # NONE/NEED(不需要/需要)
    delivery_type = StringType()  # EMP/EMS(格式为EMP/EMS/FRP 多个由/隔开 配送类型，免费快递：FRP，快递到付：EMS，快递预付：EMP)
    need_exchange = StringType()  # NONE/NEED(不需要/需要)
    ticket_get_type = StringType()  # STE/ATE(需旅客到指定地点自行换票、需到景区门口换票)
    address_details = ListType(ModelType(AddressDetail))  # 自取地址
    need_choose_address = BooleanType()  # true/false是否需要旅客在预定填写时选择自取地址
    usage_desc = StringType()  # 使用方式（内容描述）
    need_leader_card = BooleanType()  # true/false是否需要旅客的身份证明
    usage_code = StringType()  # 使用方式VOUCHER_E/VOUCHER_PAPER_ONLY/ VOUCHER_ID_ONLY(电子凭证/纸质凭证/需要旅客证件)
    ticket_type = StringType()  # 产品使用类型
    notice = StringType()  # 使用注意事项
    use_tips = ListType(StringType())  # 使用提示

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "address_details":
                new_v = AddressDetail.new_from_api(data={'address_details': v})
            if the_key in ['need_choose_address', 'need_leader_card']:
                new_v = v == 'true'
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'voucher_info' in data):
            return None

        info = data['voucher_info']
        return cls.new_from_info(info)


class AdditionalOption(Model):
    option_code = StringType()  # 附加选项的code
    option_name = StringType()  # >附加选项的名字
    desc = StringType()  # 描述
    price = StringType()  # 价格
    group = StringType()  # 分组
    unit = StringType()  # 单位（人/个/份）
    min = StringType()  # 最小购买数
    max = StringType()  # 最大购买数

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'additional_options' in data):
            return []

        infos_node = data['additional_options']
        infos = ensure_list(infos_node.get('additional-option', []))
        return [cls.new_from_info(info) for info in infos]


class AdditionalOptionGroup(Model):
    additional_options = ListType(ModelType(AdditionalOption))  # 附加选项

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "additional_options":
                new_v = AdditionalOption.new_from_api(data={'additional_options': v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'additional_option_groups' in data):
            return []

        infos_node = data['additional_option_groups']
        infos = ensure_list(infos_node.get('additional-option-group', []))
        return [cls.new_from_info(info) for info in infos]


class SaleItemDetail(Model):
    max_book_num = StringType()  # 最大预订数(假设此项目有成人、儿童、婴儿，则3个规格的购买总数不大于最大预订数)， int型，0表示没有限制
    sale_code = StringType()  # 销售项目code
    product_code = StringType()  # 产品code
    sale_name = StringType()  # 销售项目名称
    desc = StringType()  # 描述
    net_price_from = StringType()  # 净价起
    retail_price_from = StringType()  # 市场价起
    book_method = StringType()  # 预定方式（NO_CONFIRM立即确认，NEED_CONFIRM需要确认）使用book接口的时候，立即确认的产品会直接返回预订的结果，需要确认的产品会返回状态2-订单已提交
    supply_method = StringType()  # 出票方式（NO_CONFIRM立即出票，NEED_CONFIRM需要确认）使用confirm接口的时候，立即出票的产品会直接返回出票的结果，需要确认的产品会返回订单状态5-已提交确认
    pay_time = StringType()  # 此项目调用book预订接口后需要在此时间内确认,单位为秒(例:3600)，目前产品均为3600秒
    valid_time_desc = StringType()  # 有效期描述
    restriction = StringType()  # 限制
    voucher_info = ModelType(VoucherInfo)  # 凭证信息，换取方式，自取方式等
    inclusion = StringType()  # 费用包含
    exclusion = StringType()  # 费用不包含
    choose_date_method = StringType()  # ONE:只传旅行日期，TWO需要传结束日期（酒店），NONE：传当天即可
    additional_options = ListType(ModelType(AdditionalOption))  # 附加选项
    additional_option_groups = ListType(ModelType(AdditionalOptionGroup))  # 附加选项组，与附加选项的区别是，这里 是多个选项只能选择购买一种选项
    extend_properties = ListType(ModelType(ExtendProperty))  # 扩展字段

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "voucher_info":
                new_v = VoucherInfo.new_from_api(data={'voucher_info': v})
            if the_key == "additional_options":
                new_v = AdditionalOption.new_from_api(data={'additional_options': v})
            if the_key == 'additional_option_groups':
                new_v = AdditionalOptionGroup.new_from_api(data={'additional_option_groups': v})
            if the_key == 'extend_properties':
                new_v = ExtendProperty.new_from_api(data={'extend_properties': v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'sale_item_details' in data):
            return []
        infos_node = data['sale_item_details']
        infos = ensure_list(infos_node.get('sale-item-detail', []))
        return [cls.new_from_info(info) for info in infos]


class GetSaleItemDetail(Model):
    sale_item_details = ListType(ModelType(SaleItemDetail))  # 可重复节点
    product_specifications = ListType(ModelType(ProductSpecification))  # 同产品详情接口

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == 'sale_item_details':
                new_v = SaleItemDetail.new_from_api(
                    data={"sale_item_details": info['sale-item-details']}
                )
            if the_key == 'product_specifications':
                new_v = ProductSpecification.new_from_api(
                    data={"product_specifications": info['product-specifications']}
                )
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not data:
            return None

        return cls.new_from_info(data)


class Price(Model):
    sale_code = StringType()  # 销售项目code
    specification_id = StringType()  # 规格id
    net_price = StringType()  # 净价
    retail_price = StringType()  # 市场价
    fee = StringType()  # 服务费
    min_num = StringType()  # 最小购买数
    max_num = StringType()  # 最大购买数
    quota = StringType()  # 配额(-1表示无限制,0表示无配额,大于0表示配额数)
    date = StringType()  # 旅行日期
    available = BooleanType()  # 是否可退
    cancellation = StringType()  # 退具体条款
    cancel_hours = StringType()  # 提前申请小时/天数
    cancel_time_unit = StringType()  # H(小时数)/D(天数)
    cancel_type = StringType()  # NO_REFUND(不可退订)/PART_REFUND(退订收费)/RETIRE_REFUND(免费退订)

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key in ['available', 'need_leader_card']:
                new_v = v == 'true'
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not data or 'prices' not in data:
            return []

        infos_node = data['prices']
        infos = ensure_list(infos_node.get('price', []))
        return [cls.new_from_info(info) for info in infos]


class DailyPrices(Model):
    date = StringType()
    prices = ListType(ModelType(Price))

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            if the_key == 'prices':
                v = Price.new_from_api(data={"prices": v})
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'prices-collection' in data):
            return []

        info_nodes = data['prices-collection']
        infos = ensure_list(info_nodes.get('daily-prices', []))
        return [cls.new_from_info(info) for info in infos]


class PickDropModel(Model):
    type = StringType()  # 接PICKUP/送DROPOFF
    time = StringType()  # 接送的时间
    location = StringType()  # 地点
    address = StringType()  # 具体地址
    code = StringType()  # 地点的code，预订时 传入

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'picks_or_drops' in data):
            return []

        info_nodes = data['picks_or_drops']
        infos = ensure_list(info_nodes.get('pick-drop-model', []))
        return [cls.new_from_info(info) for info in infos]


class ProductPickInfo(Model):
    productCode = StringType()  # 产品code<
    picks = ListType(ModelType(PickDropModel))  # 可重复节点
    drops = ListType(ModelType(PickDropModel))  # 可重复节点

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key in ["picks", "drops"]:
                new_v = PickDropModel.new_from_api(data={"picks_or_drops": v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'product-pick-infos' in data):
            return []

        infos_node = data['product-pick-infos']
        infos = ensure_list(infos_node.get('product-pick-info', []))
        return [cls.new_from_info(info) for info in infos]


class PriceSegment(Model):
    sale_code = StringType()  # 产品代码
    sale_begin = StringType()  # 销售项目code
    sale_end = StringType()  # 销售日期起
    travel_begin = StringType()  # 出行日期起
    travel_end = StringType()  # 出行日期止
    min_advance_days = StringType()  # 最小提前购买天数
    prices = ListType(ModelType(Price))  # 价格 多个

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v

            if the_key == "prices":
                new_v = Price.new_from_api(data={'prices': v})
            setattr(rv, the_key, new_v)
        return rv


class PricesCollection(Model):
    price_segments = ListType(ModelType(PriceSegment))  # 价格段 多个

    @classmethod
    def new_from_api(cls, data):
        rv = cls()
        if not (data and 'prices-collection' in data):
            return rv

        infos_node = data['prices-collection']
        infos = ensure_list(infos_node.get('price-segment', []))
        rv.price_segments = [PriceSegment.new_from_info(info) for info in infos]
        return rv


class UnitPrice(Model):
    code = StringType()  # 规格id或者附加选项code
    price = StringType()  # 价格

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'prices' in data):
            return []

        infos_node = data['prices']
        infos = ensure_list(infos_node.get('unit-price', []))
        return [cls.new_from_info(info) for info in infos]


class Availability(Model):
    # available = StringType()  # 是否可售
    available = BooleanType()  # 是否可售
    remark = StringType()  # 备注
    total_net_price = StringType()  # 总价
    prices = ListType(ModelType(UnitPrice))  # 每个规格或者附件选项的单价

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "prices":
                new_v = UnitPrice.new_from_api(data={'prices': v})
            if the_key == 'available':
                new_v = v == 'true'
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not data:
            return None

        return cls.new_from_info(data)


class NameLanguage(Model):
    language_code = StringType()  # 支持的旅客姓名语言编码(English/Chinese)
    language_name = StringType()  # 支持的旅客姓名语言名称(英文或拼音/中文)

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'name_languages' in data):
            return []

        infos_node = data['name_languages']
        infos = ensure_list(infos_node.get('name-language', []))
        return [cls.new_from_info(info) for info in infos]


class IdentityType(Model):
    identity_code = StringType()  # 支持的证件编码（passport/permit/TEP/IDC）
    identity_name = StringType()  # 支持的证件名称(护照/港澳通行证/入台证/身份证)

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'identity_types' in data):
            return []

        infos_node = data['identity_types']
        infos = ensure_list(infos_node.get('identity-type', []))
        return [cls.new_from_info(info) for info in infos]


class DeliveryType(Model):
    delivery_code = StringType()  # EMP/FRP/EMS/SDD
    delivery_name = StringType()  # 快递预付/免费快递/快递到付/自取

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'delivery_types' in data):
            return []

        infos_node = data['delivery_types']
        infos = ensure_list(infos_node.get('delivery-type', []))
        return [cls.new_from_info(info) for info in infos]


class Question(Model):
    code = StringType()  # 问题编码
    content = StringType()  # 问题内容
    required = BooleanType()  # 是否必须回

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key in ['required']:
                new_v = v == 'true'
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'questions' in data):
            return []

        infos_node = data['questions']
        infos = ensure_list(infos_node.get('question', []))
        return [cls.new_from_info(info) for info in infos]


class TravellerLimit(Model):
    need_traveler_info = BooleanType()  # 是否需要旅客信息,需要的话在预订时传入traveller节点
    need_nationality = BooleanType()  # 是否需要旅客国籍
    need_birthday = BooleanType()  # 是否需要旅客生日
    need_gender = BooleanType()  # 是否需要旅客性别
    need_identity_expire_date = BooleanType()  # 是否需要旅客证件有效期
    need_all_traveler = BooleanType()  # 是否需要所有旅客信息,false的话只需填写一位旅客信息，true需要填写每一位的信息
    need_leader = BooleanType()  # 是否需要领队，需要的话在预订时传入leader节点，leader也算作traveller
    name_languages = ListType(ModelType(NameLanguage))  # 可重复节点
    identity_types = ListType(ModelType(IdentityType))  # 可重复节点

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "name_languages":
                new_v = NameLanguage.new_from_api(data={'name_languages': v})
            if the_key == "identity_types":
                new_v = IdentityType.new_from_api(data={'identity_types': v})
            if the_key == "questions":
                new_v = Question.new_from_api(data={'questions': v})
            if the_key in ['need_traveler_info', 'need_nationality', 'need_birthday',
                           'need_gender', 'need_identity_expire_date', 'need_all_traveler',
                           'need_leader', 'pickup_on_demand', 'dropoff_on_demand', 'pickup']:
                new_v = v == 'true'
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and "traveler_limits" in data):
            return None

        return cls.new_from_info(data['traveler_limits'])


class BookLimit(Model):
    max_book_num = StringType()  # 最大预订数(假设此项目有成人、儿童、婴儿，则3个规格的购买总数不大于最大预订数)， int型，0表示没有限制
    sale_code = StringType()  # 销售编码
    traveler_limits = ModelType(TravellerLimit)  # 旅客信息限制
    delivery_types = ListType(ModelType(DeliveryType))  # 支持的快递类型
    pickup_on_demand = BooleanType()     # 是否接受客人自填接人地址
    dropoff_on_demand = BooleanType()    # 是否接受客人自填送人地址
    pickup = BooleanType()               # 是否接人
    questions = ListType(ModelType(Question))

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "traveler_limits":
                new_v = TravellerLimit.new_from_api(data={'traveler_limits': v})
            if the_key == 'delivery_types':
                new_v = DeliveryType.new_from_api(data={'delivery_types': v})
            if the_key == 'questions':
                new_v = Question.new_from_api(data={'questions': v})
            if the_key in ['pickup_on_demand', 'dropoff_on_demand', 'pickup']:
                new_v = v == 'true'
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'book-limits' in data):
            return []

        infos_node = data['book-limits']
        infos = ensure_list(infos_node.get('book-limit', []))
        return [cls.new_from_info(info) for info in infos]


class BookItemResponse(Model):
    distributor_order_item_refer = StringType()  # 分销商的订项refer
    order_item_cd = StringType()  # 订项cd
    status = StringType()  # 状态
    remark = StringType()  # 备注
    total_net_price = StringType()  # 总净价
    cancellable =  BooleanType()  # 是否可退
    cancellation = StringType()  # 退条款
    cancel_hours = StringType()  # 退提前申请小时
    cancel_all = BooleanType()  # 是否必须整单全退
    prices = ListType(ModelType(UnitPrice))  # 每个规格或者附加选项的单价

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "prices":
                new_v = UnitPrice.new_from_api(data={'prices': v})
            if the_key in ['cancellable', 'cancel_all']:
                new_v = v == 'true'
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'book_item_responses' in data):
            return []

        infos_node = data['book_item_responses']
        infos = ensure_list(infos_node.get('book-item-response', []))
        return [cls.new_from_info(info) for info in infos]


class Book(Model):
    order_cd = StringType()  # 订单cd<
    distributor_order_refer = StringType()  # 分销商订单refer
    pay_time = StringType()  # 最晚确认时间格式 ：yyyy-mm-dd hh:mm:ss ,需在此时间之前确认，过时将返回确认失败，需重新预订
    book_item_responses = ListType(ModelType(BookItemResponse))

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "book_item_responses":
                new_v = BookItemResponse.new_from_api(data={'book_item_responses': v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not data:
            return []

        return cls.new_from_info(data)


class RefundStatus(Model):
    status = StringType()
    order_item_cd = StringType()
    refund_item_cd = StringType()

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'refund_statuses' in data):
            return []

        infos_node = data['refund_statuses']
        infos = ensure_list(infos_node.get('refund-status', []))
        return [cls.new_from_info(info) for info in infos]


class OrderItemStatus(Model):
    distributor_order_item_refer = StringType()  # 分销商订单refer
    order_item_cd = StringType()  # 订项cd
    status = StringType()  # 状态code
    remark = StringType()  # 备注
    voucher_urls = ListType(StringType())  # 凭证url
    refund_statuses = ListType(ModelType(RefundStatus))  # 退订状态

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "refund_statuses":
                new_v = RefundStatus.new_from_api(data={'refund_statuses': v})
            if the_key == 'voucher_urls':
                new_v = ensure_list(v.get('voucher-url', []))
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'order_items' in data):
            return []

        infos_node = data['order_items']
        infos = ensure_list(infos_node.get('order-item-status', []))
        return [cls.new_from_info(info) for info in infos]


# class OrderItem(Model):
#     order_item_status = ListType(ModelType(OrderItemStatus))

#     @classmethod
#     def new_from_api(cls, data):
#         rv = cls()
#         if data and 'order_items' in data:
#             infos_node = data['order_items']
#             infos = ensure_list(infos_node.get('order-item-status', []))
#             rv.order_item_status = [OrderItemStatus.new_from_info(info) for info in infos]
#         return rv


class OrderStatus(Model):
    order_cd = StringType()  # 订单cd
    distributor_order_refer = StringType()  # 分销商订单refer
    # order_items = ModelType(OrderItem)
    order_items = ListType(ModelType(OrderItemStatus))

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "order_items":
                new_v = OrderItemStatus.new_from_api(data={"order_items": v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not (data and 'order-statuses' in data):
            return []

        info_nodes = data['order-statuses']
        infos = ensure_list(info_nodes.get('order-status', []))
        return [cls.new_from_info(info) for info in infos]


class Refund(Model):
    order_cd = StringType()  # 订单cd
    distributor_order_item_refer = StringType()  # 分销商的订项refer
    status = StringType()  # 状态
    # order_items = ModelType(OrderItem)
    order_items = ListType(ModelType(OrderItemStatus))

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "order_items":
                new_v = OrderItemStatus.new_from_api(data={"order_items": v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not data:
            return None
        return cls.new_from_info(data)


# class ConfirmItem(Model):
#     order_item_status = ListType(ModelType(OrderItemStatus))

#     @classmethod
#     def new_from_api(cls, data):
#         rv = cls()
#         if data and 'confirm_items' in data:
#             infos_node = data['confirm_items']
#             infos = ensure_list(infos_node.get('order-item-status', []))
#             rv.order_item_status = [OrderItemStatus.new_from_info(info) for info in infos]
#         return rv


class Confirm(Model):
    order_cd = StringType()  # 订单cd
    customer_order_refer = StringType()  # 分销商订单refer
    # confirm_items = ModelType(ConfirmItem)  # 确认项目
    confirm_items = ListType(ModelType(OrderItemStatus))

    @classmethod
    def new_from_info(cls, info):
        rv = cls()
        for k, v in info.iteritems():
            the_key = k.replace('-', '_')
            new_v = v
            if the_key == "confirm_items":
                new_v = OrderItemStatus.new_from_api(data={'order_items': v})
            setattr(rv, the_key, new_v)
        return rv

    @classmethod
    def new_from_api(cls, data):
        if not data:
            return None
        return cls.new_from_info(data)


class Date(Model):
    # dates = ListType(StringType())

    @classmethod
    def new_from_api(cls, data):
        if data and 'dates' in data:
            infos_node = data['dates']
            infos = ensure_list(infos_node.get('date', []))
            return infos
        return []
