#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class Family(Enum):
    UNSPEC = 0
    UNIX = 1
    INET = 2
    AX25 = 3
    IPX = 4
    APPLETALK = 5
    NETROM = 6
    BRIDGE = 7
    AAL5 = 8
    X25 = 9
    INET6 = 10
    MAX = 12
