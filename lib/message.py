#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ipaddress import IPv4Address
from ipaddress import IPv6Address

from lib.enums.eventtypes import EventType
from lib.enums.states import State
from lib.macaddress import MacAddress


class Message():
    _address = IPv4Address("0.0.0.0")
    _ifidx = -1
    _ifname = ""
    _mac = MacAddress([-1, -1, -1, -1, -1, -1])
    _state = State.NONE
    _event = EventType.UNKNOWN

    def toObject(self):
        return {
            "Address": str(self._address.exploded),
            "InterfaceIndex": self._ifidx,
            "InterfaceName": self._ifname,
            "MacAddress": str(self._mac),
            "State": self._state.value,
            "EventType": self._event.value,
        }

    def __repr__(self):
        return self._representation()

    def __str__(self):
        return self._representation()

    def _representation(self):
        return "{} {} {} {} {} {}".format(self._event, self._mac, self._address.exploded, self._state, self._ifidx,
                                          self._ifname)

    def setEventType(self, event: EventType):
        self._event = event

    def setInterfaceIndex(self, ifidx: int):
        self._ifidx = ifidx

    def setInterfaceName(self, ifname: str):
        self._ifname = ifname

    def setState(self, state: State):
        self._state = state

    def setMacAddress(self, mac: MacAddress):
        self._mac = mac

    def getAddress(self):
        return self._address


class IPv4Message(Message):
    def setAddress(self, addr: IPv4Address):
        self._address = addr


class IPv6Message(Message):
    def setAddress(self, addr: IPv6Address):
        self._address = addr
