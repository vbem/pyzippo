#!/usr/bin/env python3
# coding: utf-8
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Utilities to process pure URL.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
__all__     = []
__version__ = (0, 1, 0, 'alpha', 0)
__author__  = 'vbem <i@lilei.tech>'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import re
import urllib.parse
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# https://tools.ietf.org/html/rfc1808.html
PATTERN_URL = re.compile(r'''^
    (
        (?P<scheme> [a-z]+)
        ://
    )?
    (?P<netloc>
        (
            (?P<username> [^/:@]+)
            (
                :
                (?P<password> [^/:@]+)
            )?
            @
        )?
        (?P<hostname>
            (?P<domain> ((?!-)[a-z0-9-]+(?!-)\.)+ [a-z]{2,} )
            |
            (?P<ip> [0-9]{1,3} (\.[0-9]){1,3})
        )
        (
            :
            (?P<port> [0-9]{1,5})
        )?
    )
    (?P<relpath>
        (?P<path>/[^;?#]*)
        (
            ;
            (?P<params>[^?#]*)
        )?
        (
            \?
            (?P<query>[^#]*)
        )?
    )?
    (
        \#
        (?P<fragment>.*)
    )?
$''', re.VERBOSE | re.IGNORECASE)

# https://www.ietf.org/rfc/rfc5322.txt
PATTERN_EMAIL = re.compile(r'''^
    (?P<username>[a-zA-Z0-9_.+-]+)
    @
    (?P<hostname>
        (?P<domain> ((?!-)[a-z0-9-]+(?!-)\.)+ [a-z]{2,} )
        |
        (?P<ip> [0-9]{1,3} (\.[0-9]){1,3})
    )
$''', re.VERBOSE | re.IGNORECASE)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# original path <-> escaped path
decodePath = urllib.parse.unquote
encodePath = urllib.parse.quote

# original value <-> HTML form value in a query string
decodeValue = urllib.parse.unquote_plus
encodeValue = urllib.parse.quote_plus

# list of query key-value pairs <-> query string
decodeQuery = urllib.parse.parse_qsl
encodeQuery = urllib.parse.urlencode

# hostname, port, username, password <-> netloc
decodeNetloc = urllib.parse.urlparse
def encodeNetloc(sHostname, nPort=None, sUsername=None, sPassword=None):
    r'''(hostname, port, username, password) -> netloc
    '''
    sPort = '' if nPort is None else ':{nPort}'.format_map(locals())
    if sUsername:
        if sPassword:
            sAuth = '{sUsername}:{sPassword}@'.format_map(locals())
        else:
            sAuth = '{sUsername}@'.format_map(locals())
    else:
        sAuth = ''
    return '{sAuth}{sHostname}{sPort}'.format_map(locals())

# tuple(scheme, netloc, path, params, query, fragment ) <-> URL string
decodeUrl = urllib.parse.urlparse
encodeUrl = urllib.parse.urlunparse

# base URL + relative URL -> absolute URL
joinBaseRel = urllib.parse.urljoin

# URL string -> tuple(URL-without-fragment, fragment)
defragUrl = urllib.parse.urldefrag
