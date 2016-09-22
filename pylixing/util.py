# -*- coding: utf-8 -*-
import datetime
import logging
import re

logger = logging.getLogger(__name__)


def to_json_dict(d):
    """Convert a dict-like object to a :class:`~pydida.utils.JsonDict` object"""
    assert isinstance(d, dict)
    rv = JsonDict()
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = to_json_dict(v)
        rv[str(k)] = v
    return rv


class JsonDict(dict):
    """JsonDict is a dict that allows accessing items like class attribute"""

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('JsonDict object has no attribute "%s"' % key)

    def __setattr__(self, key, value):
        self[key] = value


class cached_property(object):
    """A property that is only computed once per instance and then replaces
    itself with an ordinary attribute. Deleting the attribute resets the property.
    """

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def ensure_date_str(d, fmt='%Y-%m-%d'):
    """Try to make sure the returned value is a date string.

    :param d: `datetime.date` object, or a date string formatted with `fmt`
    :param fmt: date format, used if `d` is instance of `datetime.date`
    """
    if isinstance(d, datetime.date):
        return d.strftime(fmt)
    if isinstance(d, basestring):
        return d
    raise TypeError('Expect datetime.date or basestring, got "%r"', type(d))


def date_range_str(date_range, from_key='from', to_key='to'):
    """Generate date range parameters used by XML template.

    The result will be string like: `'from="2015-10-10" to="2015-10-12"'`

    :param date_range: A dict object probably contains `from_key` and `to_key`
    :param from_key: the key used to get from-date
    :param to_key: the key used to get to-date
    """
    rv = ''
    if not date_range:
        return rv
    if from_key in date_range:
        from_date = ensure_date_str(date_range[from_key])
        rv += 'from="%s"' % from_date
    if to_key in date_range:
        to_date = ensure_date_str(date_range[to_key])
        rv += ' to="%s"' % to_date
    return rv


def ensure_list(value):
    if not value:
        return []
    if not isinstance(value, list):
        return [value]
    return value


def has_keys(dct, keys):
    """Check if a dict has all given keys

    :param dct: dict object
    :param keys: list of keys
    """
    dict_keys = set(dct.iterkeys())
    return dict_keys.issuperset(set(keys))


def utf8(value):
    """Converts a string argument to a byte string.

    If the argument is already a byte string or None, it is returned unchanged.
    Otherwise it must be a unicode string and is encoded as utf8.

    Taken from `tornado.escape.utf8`.
    """
    if isinstance(value, bytes):
        return value
    if not isinstance(value, unicode):
        raise TypeError('Expected bytes, unicode; got %r' % type(value))
    return value.encode('utf-8')


def join_lines(data):
    return ''.join(line.strip('\t\t ') for line in data.splitlines())


def clean_xml(xml_data):
    remove_re = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]')
    new_xml_data, _ = remove_re.subn('', xml_data)
    return new_xml_data


def validate_date(begin_date, end_date):
    date_format = "%Y-%m-%d"

    if isinstance(begin_date, basestring) and isinstance(end_date, basestring):
        try:
            begin = datetime.datetime.strptime(begin_date, date_format).date()
            end = datetime.datetime.strptime(end_date, date_format).date()
            now = datetime.datetime.now().date()

            begin_from_now_days = (now - begin).days
            between_days = (end - begin).days
            if between_days < 0 or between_days > 31 or begin_from_now_days > 2:
                return False

            return True
        except:
            return False

    return False


def fake_timing(method, delta):
    logger.debug("timing: %s %sms", method, delta)
