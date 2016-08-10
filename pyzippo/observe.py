#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities for code observation.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import pprint
import itertools
import functools
import logging
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def colorize(sText, nFore=None, nBack=None, nAttr=None):
    r"""Colorize text.
    forecolors:  grey_30, red_31, green_32, yellow_33, blue_34, magenta_35, cyan_36, white_37.
    backgrounds: grey_40, red_41, green_42, yellow_43, blue_44, magenta_45, cyan_46, white_47.
    attributes:  bold_1, dark_2, underline_4, blink_5, reverse_7, concealed_8.
    """
    if not isinstance(sText, str):
        raise TypeError('{sText!r} is not str type'.format(**locals()))
    for nValue in (nFore, nBack, nAttr):
        if not (nValue is None or isinstance(nValue, int)):
            raise TypeError('argument value {nValue!r} is not valid'.format(**locals()))
    if os.getenv('ANSI_COLORS_DISABLED') is None and any((nFore, nBack, nAttr)):
        sFmtHead, sFmtTail = '\033[', 'm'
        sFmt = ';'.join((str(nValue) for nValue in (nFore, nBack, nAttr) if nValue is not None))
        return '{sFmtHead}{sFmt}{sFmtTail}{sText}{sFmtHead}{sFmtTail}'.format(**locals())
    return sText

# demo logging format string
# usage: `your_formatter = logging.Formatter(fmt=this_module.LOG_FMT)`
LOG_FMT_WHITE = '[%(asctime)s %(levelname)s %(name)s %(module)s:%(funcName)s:%(lineno)d] %(message)s'
LOG_FMT_COLOR = '{}{}{}{}{}{} %(message)s'.format(
    colorize('%(asctime)s', None, 42),
    colorize('%(levelname)s', None, 41),
    colorize('%(name)s', None, 43),
    colorize('%(module)s', None, 44),
    colorize('%(funcName)s', None, 45),
    colorize('%(lineno)s', None, 46),
)

# demo logging formater
# usage: `your_handler.setFormatter(this_module.LOG_FORMATTER)`
LOG_FORMATTER = logging.Formatter(LOG_FMT_WHITE)

# demo logging handler to stderr
# usage: `your_logger.addHandler(this_module.LOG_HANDLER_STDERR)`
LOG_HANDLER_STDERR = logging.StreamHandler()
LOG_HANDLER_STDERR.setFormatter(LOG_FORMATTER)

def getPretty(*t, **d):
    r"""Return "pretty-print" string for an object using `pprint.pformat()`.
    Default `indent` is 4.
    """
    if 'indent' not in d and len(t) < 2:
        d['indent'] = 4
    return pprint.pformat(*t, **d)

def reprArgs(*t, **d):
    r'''Return arguments' representation string as in scrpit's function invocation.
    '''
    return '({})'.format(', '.join(itertools.chain( # chain generators, then join with comma, finally enclosed
        (repr(arg) for arg in t),   # Generator of positional arguments
        ('{}={!r}'.format(*tKv) for tKv in d.items()), # Generator of keyword arguments
    )))

def getFuncFullName(func):
    r'''Return `package-name.module-name.class-name.method-name` like qualified name of given function object.
    '''
    if not callable(func):
        raise TypeError('{func!r} is not callable'.format(**locals()))
    return '{}.{}'.format(func.__module__, func.__qualname__)

def logCall(logger=_LOGGER, nLevel=logging.DEBUG):
    r'''A decorator wraps longging on function call's begin and end with given logger and level .
    '''
    if not isinstance(logger, logging.Logger):
        raise TypeError('{logger!r} is not a logging.Logger instance'.format(**locals()))
    if not isinstance(nLevel, int) or nLevel not in logging._levelToName:
        raise ValueError('{nLevel!r} is not a valid logging level'.format(**locals()))
    def decorator(func):
        sFunc = getFuncFullName(func)
        @functools.wraps(func)
        def wrapper(*t, **d):
            nonlocal sFunc
            sArgs = reprArgs(*t, **d)
            logger.log(nLevel, '%(sFunc)s <= %(sArgs)s', locals())
            result = func(*t, **d)
            logger.log(nLevel, '%(sFunc)s => %(result)r', locals())
            return result
        return wrapper
    return decorator