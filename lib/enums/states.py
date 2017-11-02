#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum, unique

@unique
class State(Enum):
    NONE = 0x00
    INCOMPLETE = 0x01
    REACHABLE = 0x02
    STALE = 0x04
    DELAY = 0x08
    PROBE = 0x10
    FAILED = 0x20
    NOARP = 0x40
    PERMANENT = 0x80
