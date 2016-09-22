# -*- coding: utf-8 -*-
import time
import logging

from .exceptions import ConnectionError


class retry_on_error(object):
    def __init__(self, max_retries=3, delay=0.1, backoff=2):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def is_server_error(resp):
        return 500 <= resp.status_code <= 599

    def _sleep(self, tries, delay):
        self.logger.warn('retry [%d], delay: %s ms', tries, delay * 1000)
        time.sleep(delay)
        return delay * self.backoff

    def __call__(self, func):
        def decorator(*args, **kwargs):
            delay = self.delay
            tries = 0
            while tries < self.max_retries:
                tries += 1
                try:
                    resp = func(*args, **kwargs)
                except ConnectionError as exc:
                    if tries == self.max_retries:
                        raise exc
                    delay = self._sleep(tries, delay)
                    continue

                if not self.is_server_error(resp) or tries == self.max_retries:
                    return resp

                delay = self._sleep(tries, delay)

        return decorator
