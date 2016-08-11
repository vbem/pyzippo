#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities for numerial computing.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def _assertIsNumerial(**d):
    r'''Assert key arguments are numerial, otherwise, raise TypeError.
    '''
    for k, v in d.items():
        if not isinstance(v, (int, float)):
            raise TypeError('{k}={v!r} is neither `int` nor `float`'.format_map(locals()))

def approximate(nA, nB, nDelta=1e-7):
    r'''Check if number `nA` and `nB` are approximately equal with given delta.
    '''
    _assertIsNumerial(nA=nA, nB=nB, nDelta=nDelta)
    return nA is nB or nA==nB or abs(nA - nB) <= nDelta
