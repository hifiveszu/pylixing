# -*- coding: utf-8 -*-
from schematics.models import Model
from schematics.types import StringType, FloatType

from ..util import ensure_list


class Location(Model):
    type = StringType()  # 可选值：COUNTRY, CITY, REGION
    short_name = StringType()  # ISO 代码
    name = StringType()  # 英文名
    name_cn = StringType()  # 中文名
    code = StringType()  # 力行编码
    parent_code = StringType()  # 父级编码
    look_up_code = StringType()  # 查找编码（从最高级到本级的code 集合 用,隔开）
    lon = FloatType()  # 经度
    lat = FloatType()  # 纬度
    hot = StringType()

    @property
    def is_hot(self):
        return self.hot == 'Y'

    @classmethod
    def new_from_location(cls, location):
        """把 <location></location> 节点转换成 Location 类型

        :param location: dict 类型，可能是 dict 或 OrderedDict
        """
        rv = cls()
        for k, v in location.iteritems():
            # API 返回的 XML 节点用 '-' 连接，这里换成 '_'
            the_key = k.replace('-', '_')
            setattr(rv, the_key, v)
        rv.validate()
        return rv

    @classmethod
    def new_from_api(cls, data):
        """把 <locations></locations> 转换成 [Location] 类型
        :param data: dict 类型
        """
        locations = ensure_list(data['locations'].get('location', []))
        return [cls.new_from_location(location) for location in locations]
