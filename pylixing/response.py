# -*- coding: utf-8 -*-
import xmltodict

from .util import cached_property, clean_xml


class Response(object):
    """Response object is a simple wrapper over `requests.models.Response`

    :param resp: A `requests.models.Response` object.
    """

    def __init__(self, resp):
        #: save the original response
        self._resp = resp

        #: if raw is True, self._data is the raw xml data
        self.raw = True

        #: result data, xml or some model
        if self.ok:
            # print "=" * 10, self.to_dict['response']
            # self._data = self.to_dict['response']
            self._data = self.to_dict['response'].get('payload', None)
        else:
            self._data = None

    def to_model(self, model_class):
        self._data = model_class.new_from_api(self._data)
        self.raw = False
        return self

    @property
    def status_code(self):
        """HTTP response status code"""
        return self._resp.status_code

    @property
    def ok(self):
        """If the API succeeded (``True``) or not (``False``)"""
        if not self._resp.ok:   # some HTTPError happens
            return False

        if self.api_code:
            return self.api_code == '200'
        if self.api_message:
            return self.api_message == 'OK'
        return False

    @property
    def data(self):
        return self._data

    @property
    def api_code(self):
        """<status-code><status-code> from returned xml."""
        if not self._resp.ok:
            return str(self.status_code)
        return self.to_dict['response'].get('status-code')

    @property
    def api_message(self):
        """<status-message></status-message> from returned xml."""
        if not self._resp.ok:
            return self._resp.reason
        return self.to_dict['response'].get('status-message')

    @property
    def request_time(self):
        """Elapsed time in milliseconds."""
        return self._resp.elapsed.total_seconds() * 1000

    @property
    def to_xml(self):
        """Returns the raw response content, which is in XML format"""
        return clean_xml(self._resp.content)

    @cached_property
    def to_dict(self):
        """Converts response content into ``dict``
        (which is indeed :class:`~collections.OrderedDict`)"""
        return xmltodict.parse(self.to_xml)

    def __str__(self):
        status = 'code: %s, message: %s' % (self.api_code, self.api_message)
        return '<Response (%d, "%s")>' % (self.status_code, status)

    __repr__ = __str__
