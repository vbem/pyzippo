#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities for debugging.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import pprint
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getPretty(*t, **d):
    r"""Return "pretty-print" string for an object using `pprint.pformat()`.
    Default `indent` is 4.
    """
    if 'indent' not in d and len(t) < 2:
        d['indent'] = 4
    return pprint.pformat(*t, **d)
