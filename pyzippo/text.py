#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities for text.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import enum
import itertools
import textwrap
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

@enum.unique
class Color(enum.IntEnum):
    r'''Colorize text.
    '''
    # forecolors
    F_GREY      = 30
    F_RED       = 31
    F_GREEN     = 32
    F_YELLOW    = 33
    F_BLUE      = 34
    F_MAGENTA   = 35
    F_CYAN      = 36
    F_WHITE     = 37

    # backgrounds
    B_GREY      = 40
    B_RED       = 41
    B_GREEN     = 42
    B_YELLOW    = 43
    B_BLUE      = 44
    B_MAGENTA   = 45
    B_CYAN      = 46
    B_WHITE     = 47

    # attributes
    A_BOLD      = 1
    A_DARK      = 2
    A_UNDERLINE = 4
    A_BLINK     = 5
    A_REVERSE   = 7
    A_CONCEALED = 8

    @classmethod
    def render(cls, s, *t):
        r"""Colorize text with given arguments of this enumeration's' colors.
        """
        if not isinstance(s, str):
            raise TypeError('{s!r} is not str type'.format_map(locals()))
        lColorInt = []
        for each in t:
            if isinstance(each, cls):
                lColorInt.append(each.value)
            elif isinstance(each, str):
                lColorInt.append(cls[each].value)
            elif isinstance(each, int):
                lColorInt.append(cls(each).value)
            else:
                raise TypeError('{each!r} is not valid a color argument'.format_map(locals()))

        if lColorInt and os.getenv('ANSI_COLORS_DISABLED') is None:
            sFmtHead, sFmtTail = '\033[', 'm'
            sFmt = ';'.join(str(n) for n in lColorInt)
            return '{sFmtHead}{sFmt}{sFmtTail}{s}{sFmtHead}{sFmtTail}'.format_map(locals())
        return s

def reprArgs(*t, **d):
    r'''Return arguments' representation string as in scrpit's function invocation.
    '''
    return '({})'.format(', '.join(itertools.chain( # chain generators, then join with comma, finally enclosed
        (repr(arg) for arg in t),   # Generator of positional arguments
        ('{}={!r}'.format(*tKv) for tKv in d.items()), # Generator of keyword arguments
    )))

def shrink(s):
    r"""Shrink a text by `textwrap.detent` and then `str.strip`.
    """
    if not isinstance(s, str):
        raise TypeError('{s!r} is not str type'.format_map(locals()))
    return textwrap.dedent(s).strip()