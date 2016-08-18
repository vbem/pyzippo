#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities for threading.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import queue
import threading
import urllib.request
import logging

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
LOG = logging.getLogger(__name__)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class MultiThreads(list):
    def __init__(self, nSize, **d):
        super().__init__() # empty list
        for n in range(nSize):
            self.append(threading.Thread(name='{}-{}/{}'.format(d['target'].__name__, n+1, nSize), **d))

    def start_all(self, *t, **d):
        for thread in self:
            thread.start(*t, **d)

    def join_all(self, *t, **d):
        for thread in self:
            thread.join(*t, **d)

class Crawler:
    r'''Crawler multi-threading join based.
    '''
    def __init__(self, iterUrls, nThreadsSize, nTimeout=None, *t, **d):
        r"""Initialization.
        """
        super().__init__(*t, **d)
        self._iterUrls = iterUrls
        self._nThreadsSizeUrls = 1
        self._nThreadsSizeResponses = nThreadsSize
        self._nTimeoutResponses = nTimeout

    def yieldResponses(self):
        r'''
        '''
        # `_target_urls` output queue
        self._qUrls = queue.Queue(2 * max((self._nThreadsSizeUrls, self._nThreadsSizeResponses)))

        # `_target_responses` output queue
        self._qResponses = queue.Queue(2 * self._nThreadsSizeResponses)

        # `_target_urls` threads
        self._threadsUrls = MultiThreads(nSize=self._nThreadsSizeUrls, target=self._target_urls)
        self._threadsUrls.start_all()

        # `_target_responses` threads
        self._threadsResponses = MultiThreads(nSize=self._nThreadsSizeResponses, target=self._target_responses)
        self._threadsResponses.start_all()

        # `_target_sentinel` thread
        self._threadSentinel = threading.Thread(target=self._target_sentinel, name='_target_sentinel')
        self._threadSentinel.start()

        # main thread
        while True:
            tResponse = self._qResponses.get()
            LOG.debug('get {}'.format(tResponse))
            if tResponse is EOFError:
                self._threadSentinel.join() # wait `_target_sentinel` terminates
                LOG.info('finish self._threadSentinel.join()')
                break # terminate this thread
            yield tResponse

    def _target_urls(self):
        r"""
        """
        for tUrl in enumerate(self._iterUrls):
            self._qUrls.put(tUrl) # may block
            LOG.debug('{} put {}'.format(threading.current_thread().name, tUrl))
        # terminate this thread
        LOG.info('{} terminated'.format(threading.current_thread().name))

    def _target_responses(self):
        r'''
        '''
        while True:
            tUrl = self._qUrls.get() # may block
            LOG.debug('{} get {}'.format(threading.current_thread().name, tUrl))
            if tUrl is EOFError:
                LOG.info('{} terminated'.format(threading.current_thread().name))
                break # terminate this thread
            nIndex, sUrl = tUrl
            try:
                with urllib.request.urlopen(url=sUrl, timeout=self._nTimeoutResponses) as obj:
                    response = obj
            except Exception as e:
                response = e
            self._qResponses.put((nIndex, sUrl, response)) # may block
            LOG.debug('{} put {}'.format(threading.current_thread().name, (nIndex, sUrl, response)))

    def _target_sentinel(self):
        r'''
        '''
        self._threadsUrls.join_all() # wait all `_target_urls` terminates
        LOG.info('finish self._threadsUrls.join_all()')
        for thread in self._threadsResponses:
            self._qUrls.put(EOFError) # tell all `_target_responses` terminates
        LOG.info('finish self._qUrls.put(EOFError)')
        self._threadsResponses.join_all() # wait all `_target_responses` terminates
        LOG.info('finish self._threadsResponses.join_all()')
        self._qResponses.put(EOFError) # tell main thread terminates
        LOG.info('finish self._qResponses.put(EOFError)')
        # terminate this thread
        LOG.info('{} terminated'.format(threading.current_thread().name))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == "__main__":
    import journal
    LOG.addHandler(logging.NullHandler()) # as lib
    LOG.addHandler(journal.LOG_HANDLER_COLOR) # as app

    LOG.setLevel(logging.DEBUG)

    c = Crawler(['http://www.liwanshi.com/']*30, nThreadsSize=5)
    for tResponse in c.yieldResponses():
        print(tResponse)


