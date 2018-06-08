#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 20:06
# @Author  : jiakang
# @File    : __totp.py
# @Software: IntelliJ IDEA

"""Implementation of RFC 4226: HMAC-Based One-Time Password Algorithm (HTOP),
and RFC 6238: Time-Based One-Time Password Algorithm (TOTP).
"""

__author__ = 'acoster'
__copyright__ = 'Copyright 2012, Alexandre Coster'

import hmac
import time
import base64
import struct
import hashlib


def get_hotp(secret, counter):
    """Return the HMAC-Based One-Time Password for the the given secret (base32 encoded) and the counter.
    >>> [get_hotp('GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ', i) for i in xrange(10)]
    [755224, 287082, 359152, 969429, 338314, 254676, 287922, 162583, 399871, 520489]
    """
    secret = base64.b32decode(secret)
    counter = struct.pack('>Q', counter)

    hash = hmac.new(secret, counter, hashlib.sha1).digest()
    offset = ord(hash[19]) & 0xF

    return (struct.unpack(">I", hash[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000


def get_totp(secret):
    """Return the Time-Based One-Time Password for the current time, and the provided secret (base32 encoded)
       For obvious reasons, no unit-test is provided for this function.
    """
    return get_hotp(secret, int(time.time()) // 30)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    seed = 'T1NPSUZMS0FaQlhKUkNNWA=='
    seed_32 = base64.b64decode(seed)
    totp = get_totp(seed_32)
    print(totp)

    import commands
    totp2 = commands.getoutput('oathtool --totp -b -d 6 %s' % base64.b64decode(seed))
    print(totp2)
