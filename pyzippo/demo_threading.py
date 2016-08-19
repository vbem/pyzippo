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

class ThreadsPool(list):
    def __init__(self, nSize, clsThread=threading.Thread, **d):
        super().__init__() # empty list
        for n in range(nSize):
            sNamePrefix = d['target'].__name__ if 'target' in d else clsThread.__name__
            sName = '{}-{}/{}'.format(sNamePrefix, n+1, nSize)
            self.append(clsThread(name=sName, **d))

    def start_all(self, *t, **d):
        for thread in self:
            thread.start(*t, **d)

    def join_all(self, *t, **d):
        for thread in self:
            thread.join(*t, **d)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class ThreadUrls(threading.Thread):
    r'''Thread generates URLs.
    '''
    def __init__(self, iterUrls, qOutput, **d):
        r'''
        '''
        super().__init__(**d)
        self._iterUrls = iterUrls
        self._qOutput = qOutput

    def run(self):
        r'''
        '''
        for tUrl in enumerate(self._iterUrls):
            self._qOutput.put(tUrl) # may block
            LOG.debug('%r put %r', threading.current_thread().name, tUrl)
        LOG.info('%r terminated', threading.current_thread().name)

class ThreadResponses(threading.Thread):
    r'''Thread generates responses.
    '''
    def __init__(self, qInput, qOutput, nTimeout=None, **d):
        r'''
        '''
        super().__init__(**d)
        self._qInput = qInput
        self._qOutput = qOutput
        self._nTimeout = nTimeout

    def run(self):
        r'''
        '''
        for tUrl in iter(self._qInput.get, EOFError): # queue.Queue.get() may block
            LOG.debug('%r get %r', threading.current_thread().name, tUrl)
            nIndex, sUrl = tUrl
            try:
                with urllib.request.urlopen(url=sUrl, timeout=self._nTimeout) as obj:
                    response = obj
            except Exception as e:
                response = e
            self._qOutput.put((nIndex, sUrl, response)) # may block
            LOG.debug('%r put %r', threading.current_thread().name, (nIndex, sUrl, response))
        LOG.info('%r terminated', threading.current_thread().name)

class ThreadSentinel(threading.Thread):
    r'''Thread sentinel.
    '''
    def __init__(self, qUrls, qResponses, poolUrls, poolResponses, **d):
        r'''
        '''
        d.setdefault('name', self.__class__.__name__)
        super().__init__(**d)
        self._qUrls = qUrls
        self._qResponses = qResponses
        self._poolUrls = poolUrls
        self._poolResponses = poolResponses

    def run(self):
        r'''
        '''
        self._poolUrls.join_all()
        LOG.info('joined all poolUrls')

        for thread in self._poolResponses:
            self._qUrls.put(EOFError)
        LOG.info('told all poolResponses to terminate')
        self._poolResponses.join_all()
        LOG.info('joined all poolResponses')

        self._qResponses.put(EOFError)
        LOG.info('told main thread to terminate')
        LOG.info('%r terminated', threading.current_thread().name)
        
def yieldResponses(iterUrls, nConcurrentCount, nTimeout=None):
    r'''
    '''
    qUrls = queue.Queue(2 * nConcurrentCount)
    qResponses = queue.Queue(2 * nConcurrentCount)

    poolUrls = ThreadsPool(nSize=1, clsThread=ThreadUrls, iterUrls=iterUrls, qOutput=qUrls)
    poolUrls.start_all()

    poolResponses = ThreadsPool(nSize=nConcurrentCount, clsThread=ThreadResponses, qInput=qUrls, qOutput=qResponses, nTimeout=nTimeout)
    poolResponses.start_all()

    threadSentinel = ThreadSentinel(qUrls=qUrls, qResponses=qResponses, poolUrls=poolUrls, poolResponses=poolResponses)
    threadSentinel.start()

    # main thread
    for tResponse in iter(qResponses.get, EOFError): # queue.Queue.get() may block
        LOG.debug('main thread get %r', tResponse)
        yield tResponse
    threadSentinel.join()
    LOG.info('joined sentinel')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == "__main__":
    import journal
    LOG.addHandler(logging.NullHandler()) # as lib
    LOG.addHandler(journal.LOG_HANDLER_COLOR) # as app

    LOG.setLevel(logging.INFO)

    for nIndex, sUrl, response in yieldResponses(iterUrls=['http://www.liwanshi.com/']*100, nConcurrentCount=10):
        print(nIndex, sUrl, response)

