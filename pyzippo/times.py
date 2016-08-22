#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities to process times.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import time
import datetime
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def getAwareUTC():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

def getAwareLocal():
    return datetime.datetime.now().replace(tzinfo=LOCAL_TIMEZONE)
