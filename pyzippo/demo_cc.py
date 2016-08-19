#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities for multiprocessing.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import logging
import itertools
import concurrent.futures as cc
import urllib.request

LOG = logging.getLogger(__name__)
import journal
LOG.addHandler(logging.NullHandler()) # as lib
LOG.addHandler(journal.LOG_HANDLER_COLOR) # as app
LOG.setLevel(logging.DEBUG)
LOG.debug('in module %r',__name__)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def getResponse(nIndex, sUrl, nTimeout=None):
    LOG.debug('input %s', nIndex)
    try:
        with urllib.request.urlopen(url=sUrl, timeout=nTimeout) as obj:
            response = obj
    except Exception as e:
        response = e
    LOG.debug('output %s', nIndex)
    return nIndex, response

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == "__main__":
    with cc.ThreadPoolExecutor(max_workers=10) as executor:
        LOG.debug('now call concurrent map')
        for tReturn in executor.map(getResponse, range(100), itertools.repeat('http://lilei.tech/'), itertools.repeat(0.07), timeout=4):
            LOG.info('yield %r', tReturn)