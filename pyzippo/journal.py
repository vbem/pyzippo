#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities for logging.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import functools
import contextlib
import inspect
import logging
import weakref

import text
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# demo logging format string
# usage: `your_formatter = logging.Formatter(fmt=this_module.LOG_FMT)`
LOG_FMT_DEMO = '[%(asctime)s %(levelname)s %(name)s %(module)s:%(funcName)s:%(lineno)d] %(message)s'
LOG_FMT_COLOR = '{}{}{}{}{}{} {}'.format(
    text.Color.render('%(asctime)s',    text.Color.B_GREEN),
    text.Color.render('%(levelname)s',  text.Color.B_RED),
    text.Color.render('%(name)s',       text.Color.B_YELLOW),
    text.Color.render('%(module)s',     text.Color.B_BLUE),
    text.Color.render('%(funcName)s',   text.Color.B_MAGENTA),
    text.Color.render('%(lineno)s',     text.Color.B_CYAN),
    text.Color.render('%(message)s',    text.Color.F_GREEN),
)

# demo logging handler to stderr
# usage: `your_logger.addHandler(this_module.LOG_HANDLER)`
LOG_HANDLER_DEMO = logging.StreamHandler()
LOG_HANDLER_DEMO.setFormatter(logging.Formatter(LOG_FMT_DEMO))

LOG_HANDLER_COLOR = logging.StreamHandler()
LOG_HANDLER_COLOR.setFormatter(logging.Formatter(LOG_FMT_COLOR))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getFuncFullName(func):
    r'''Return `package-name.module-name.class-name.method-name` like qualified name of given function object.
    '''
    if not callable(func):
        raise TypeError('{func!r} is not callable'.format_map(locals()))
    return '{}.{}'.format(func.__module__, func.__qualname__)

def decorateLog(logger, nLevel=logging.DEBUG):
    r'''A decorator wraps longging on function call's begin and end with given logger and level.
    '''
    if not isinstance(logger, logging.Logger):
        raise TypeError('{logger!r} is not a logging.Logger instance'.format_map(locals()))
    if nLevel not in logging._levelToName:
        raise ValueError('{nLevel!r} is not a valid logging level'.format_map(locals()))

    def decorator(func):
        sFunc = getFuncFullName(func)

        @functools.wraps(func)
        def wrapper(*t, **d):
            nonlocal sFunc
            sArgs = text.reprArgs(*t, **d)
            logger.log(nLevel, '%(sFunc)s <= %(sArgs)s', locals())
            try:
                result = func(*t, **d)
            except BaseException as e:
                logger.log(nLevel, '%(sFunc)s raises %(e)r', locals())
                raise
            else:
                logger.log(nLevel, '%(sFunc)s => %(result)r', locals())
                return result

        return wrapper

    return decorator

@contextlib.contextmanager
def contextLog(logger, nLevel=logging.DEBUG, sName=None):
    r'''A context manager supports longging on code block begin and end with given logger, level and block name.
    '''
    if not isinstance(logger, logging.Logger):
        raise TypeError('{logger!r} is not a logging.Logger instance'.format_map(locals()))
    if nLevel not in logging._levelToName:
        raise ValueError('{nLevel!r} is not a valid logging level'.format_map(locals()))
    if sName is None:
        frameCaller = inspect.stack()[2][0] # frame of caller stack
        sCallerModuleName = frameCaller.f_locals['__name__']
        sCallerLineNo = frameCaller.f_lineno
        sName = '{sCallerModuleName}:{sCallerLineNo}'.format_map(locals())
    if not isinstance(sName, str):
        raise TypeError('{sName!r} is not a str'.format_map(locals()))

    logger.log(nLevel, 'block %(sName)r starts', locals())
    try:
        yield sName
    except BaseException as e:
        logger.log(nLevel, 'block %(sName)r raises: %(e)r', locals())
        raise
    else:
        logger.log(nLevel, 'block %(sName)r finished', locals())

class DescriptorLog:
    r'''A descriptor with logging on its access.
    '''
    def __init__(self, logger, nLevel=logging.DEBUG, sName=None, default=None):
        r'''Initialize with given name and default value.
        '''
        if not isinstance(logger, logging.Logger):
            raise TypeError('{logger!r} is not a logging.Logger instance'.format_map(locals()))
        if nLevel not in logging._levelToName:
            raise ValueError('{nLevel!r} is not a valid logging level'.format_map(locals()))
        if not isinstance(sName, str):
            raise TypeError('{sName!r} is not a str'.format_map(locals()))

        self._logger = logger
        self._nLevel = nLevel
        self._sName = sName
        self._default = default
        self._dict = weakref.WeakKeyDictionary()
        self._logger.log(self._nLevel, 'descriptor %r created', self._sName)

    def __get__(self, obj, typeObj=None):
        value = self._dict.get(obj, self._default)
        self._logger.log(self._nLevel, 'descriptor %r => %r', self._sName, value)
        return value

    def __set__(self, obj, value):
        self._dict[obj] = value
        self._logger.log(self._nLevel, 'descriptor %r <= %r', self._sName, value)

    def __delete__(self, obj):
        del self._dict[obj]
        self._logger.log(self._nLevel, 'descriptor %r deleted', self._sName)

