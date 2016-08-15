#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""A demo module using `argparse`.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import sys
import argparse
import logging

import journal
import text
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler()) # as lib
LOG.addHandler(journal.LOG_HANDLER_COLOR) # as app
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CLI functions

def runCli(lCliArgs=None):
    r'''Run CLI.
    '''
    dCommonParserInitArgs = {
        'formatter_class' : argparse.RawTextHelpFormatter,
        'epilog' : 'I/O: stdin->input, stdout->result, stderr->logging, exit code->status check',
    }

    s = text.shrink(__doc__)
    parserMain = argparse.ArgumentParser(description=s, **dCommonParserInitArgs)
    groupMutex = parserMain.add_mutually_exclusive_group()
    s = 'disable all logging messages'
    groupMutex.add_argument('-q', '--quite', action='store_true', help=s)
    s = text.shrink(r"""
        increase logging verbosity
        without this, log at `warning` level
        with `-v`, log at `info` level
        with `-vv`, log at `debug` level
    """)
    groupMutex.add_argument('-v', '--verbose', action='count', default=0, help=s)

    s = 'each sub-command for a specific task'
    actionSub = parserMain.add_subparsers(dest='subcommand', description=s)

    s = 'demo sub-command with sub-arguments'
    parserDemo = actionSub.add_parser(name='demo', description=s, help=s, **dCommonParserInitArgs)
    s = text.shrink(r"""
        an optional single item
        type: %(type)s; choices: %(choices)s; default: %(const)s
    """)
    parserDemo.add_argument('--opt-single', metavar='VAL', nargs='?', const=100, type=int, choices=range(100,600,100), help=s)
    s = 'an optional double items'
    parserDemo.add_argument('--opt-double', metavar=('FROM_FILE', 'TO_FILE'), nargs=2, help=s)
    s = 'an optional list'
    parserDemo.add_argument('--opt-list', metavar='VAL', nargs='+', help=s)

    s = 'show docs in source code'
    parserDocs = actionSub.add_parser(name='docs', description=s, help=s, **dCommonParserInitArgs)

    namespace = parserMain.parse_args(args=lCliArgs)

    if namespace.quite:
        LOG.setLevel(51)
    else:
        LOG.setLevel(logging.WARNING if namespace.verbose==0 else logging.INFO if namespace.verbose==1 else logging.DEBUG)

    LOG.debug(namespace)

    if not namespace.subcommand:
        LOG.warning('no sub-command specified, show help instead')
        parserMain.print_help()
        return 1

    if namespace.subcommand == 'docs':
        help(os.path.splitext(os.path.basename(__file__))[0])
        return 0

    if namespace.subcommand == 'demo':
        if namespace.opt_single:
            print('`demo` receive `--opt-single` with {namespace.opt_single!r}'.format_map(locals()))
            return 0
        if namespace.opt_double:
            print('`demo` receive `--opt-double` with {namespace.opt_double!r}'.format_map(locals()))
            return 0
        if namespace.opt_list:
            print('`demo` receive `--opt-list` with {namespace.opt_list!r}'.format_map(locals()))
            return 0

        LOG.warning('no valid argument for this sub-command specified, show help instead')
        parserDemo.print_help()
        return 1

    return 255

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == "__main__":
    nRet = runCli()
    LOG.info('terminates with status code: {nRet}'.format_map(locals()))
    sys.exit(nRet)