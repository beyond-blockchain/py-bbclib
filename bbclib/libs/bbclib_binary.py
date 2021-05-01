# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 beyond-blockchain.org.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import sys

import binascii
import hashlib
import random
import time
from collections.abc import Mapping

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(current_dir, "../.."))

from bbclib.libs.bbclib_config import DEFAULT_ID_LEN

from bbclib.libs.bbclib_transaction import BBcTransaction
from bbclib.libs.bbclib_signature import BBcSignature
from bbclib.libs.bbclib_asset_raw import BBcAssetRaw
from bbclib.libs.bbclib_asset_hash import BBcAssetHash
from bbclib.libs.bbclib_asset import BBcAsset
from bbclib.libs.bbclib_relation import BBcRelation
from bbclib.libs.bbclib_reference import BBcReference
from bbclib.libs.bbclib_event import BBcEvent
from bbclib.libs.bbclib_pointer import BBcPointer
from bbclib.libs.bbclib_witness import BBcWitness
from bbclib.libs.bbclib_crossref import BBcCrossRef


def str_binary(dat):
    if dat is None:
        return "None"
    else:
        return binascii.b2a_hex(dat)


def to_bigint(val, size=32):
    dat = bytearray(to_2byte(size))
    dat.extend(val)
    return dat


def to_8byte(val):
    return val.to_bytes(8, 'little')


def to_4byte(val):
    return val.to_bytes(4, 'little')


def to_2byte(val):
    return val.to_bytes(2, 'little')


def to_1byte(val):
    return val.to_bytes(1, 'little')


def get_n_bytes(ptr, n, dat):
    return ptr+n, dat[ptr:ptr+n]


def get_n_byte_int(ptr, n, dat):
    return ptr+n, int.from_bytes(dat[ptr:ptr+n], 'little')


def get_bigint(ptr, dat):
    size = int.from_bytes(dat[ptr:ptr+2], 'little')
    return ptr+2+size, dat[ptr+2:ptr+2+size]


def bin2str_base64(dat):
    import binascii
    return binascii.b2a_base64(dat, newline=False).decode("utf-8")


def bin2str_base64(dat):
    import binascii
    return binascii.b2a_base64(dat, newline=False).decode("utf-8")


def get_random_value(length=DEFAULT_ID_LEN):
    """Return random bytes

    Args:
        length (int): length of the result
    Returns:
        bytes: random bytes
    """
    val = bytearray()
    for i in range(length):
        val.append(random.randint(0,255))
    return bytes(val)
