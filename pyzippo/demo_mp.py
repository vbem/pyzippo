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
import multiprocessing as mp
import urllib.request

LOG_MP = mp.get_logger()
import journal
LOG_MP.addHandler(logging.NullHandler()) # as lib
LOG_MP.addHandler(journal.LOG_HANDLER_COLOR) # as app
LOG_MP.setLevel(logging.INFO)
LOG_MP.info('%r in %r', mp.current_process().name, __name__)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def getResponse(sUrl, nTimeout=None):
    try:
        with urllib.request.urlopen(url=sUrl, timeout=nTimeout) as obj:
            return obj
    except Exception as e:
        return e

def getResponseWraped(tArgs):
    nIndex, sUrl, nTimeout = tArgs
    LOG_MP.info('%r input %r', mp.current_process().name, nIndex)
    tReturn = nIndex, sUrl, getResponse(sUrl, nTimeout)
    import time, random
    time.sleep(random.random())

    LOG_MP.info('%r output %r', mp.current_process().name, nIndex)
    return tReturn

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == "__main__":
    LOG_MP.info('%r come in main', mp.current_process().name)
    iterArgs = ((n+1, 'http://lilei.tech/', None) for n in range(20))
        
    with mp.Pool(processes=os.cpu_count()*2) as pool:
        i = pool.imap_unordered(getResponseWraped, iterArgs, 10)
        for r in i:
            print(r)
        
