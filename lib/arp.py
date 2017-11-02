#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

log = logging.getLogger(__name__)

import signal

from time import sleep
from ipaddress import IPv4Address
from ipaddress import IPv6Address

from lib.macaddress import MacAddress
from lib.enums.families import Family
from lib.enums.states import State
from lib.enums.eventtypes import EventType

from lib.message import Message
from lib.message import IPv4Message
from lib.message import IPv6Message

from lib.notifiers.notifier import Notifier

from pyroute2 import IPDB


class ArpNetworkNeighborNotifier():
    ip = None
    _notifier = None

    def __init__(self):
        self.serve = True
        self.not_connect = True
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        if self._notifier is not None:
            log.info("Stopping notifier..")
            self._notifier.stop()

        self.stop()

        signal.signal(signal.SIGTERM, signal.SIG_IGN)

    def initlisten(self):
        if self._notifier is None:
            raise TypeError("Notifier is not set")

        ignore_tables = [254]
        self.ip = IPDB(ignore_rtables=ignore_tables)
        self.ip.register_callback(self.callback)

    def callback(self, ipdb, msg, action):
        # Add interface name
        if 'ifindex' in msg:
            with ipdb.interfaces[msg['ifindex']].ro as iface:
                msg['ifname'] = iface.ifname

        if action == 'RTM_NEWNEIGH':
            self.add_neighbour(self.generate_message(self.sanitize(msg)))
        elif action == 'RTM_DELNEIGH':
            self.remove_neighbour(self.generate_message(self.sanitize(msg)))

    def setNotifier(self, notifier: Notifier):
        log.info("Registering notifier: {}".format(type(notifier).__name__))
        self._notifier = notifier

    def sanitize(self, obj):
        delete_keys = ['__pad', 'ndm_type', 'header']

        for i in delete_keys:
            if i in obj:
                del obj[i]

        if 'state' in obj:
            obj['state'] = State(obj['state'])

        if 'family' in obj:
            obj['family'] = Family(obj['family'])

        if 'event' in obj:
            if obj['event'] == 'RTM_NEWNEIGH':
                obj['event'] = EventType.NEW
            elif obj['event'] == 'RTM_DELNEIGH':
                obj['event'] = EventType.DEL

        if 'attrs' in obj:
            obj['attrs'] = dict(obj['attrs'])

            if obj['family'] is Family.INET:
                if 'NDA_DST' in obj['attrs']:
                    obj['address'] = IPv4Address(obj['attrs']['NDA_DST'])

            if obj['family'] is Family.INET6:
                if 'NDA_DST' in obj['attrs']:
                    obj['address'] = IPv6Address(IPv6Address(obj['attrs']['NDA_DST']).exploded)

            if 'NDA_LLADDR' in obj['attrs']:
                obj['mac'] = MacAddress(obj['attrs']['NDA_LLADDR'])

            del obj['attrs']

        if 'family' in obj:
            del obj['family']

        return obj

    def generate_message(self, obj):
        o = None

        if isinstance(obj['address'], IPv4Address):
            o = IPv4Message()
            o.setAddress(obj['address'])
        elif isinstance(obj['address'], IPv6Address):
            o = IPv6Message()
            o.setAddress(obj['address'])

        if o is None:
            raise TypeError

        o.setInterfaceName(obj['ifname'])
        o.setInterfaceIndex(obj['ifindex'])
        o.setState(obj['state'])
        o.setEventType(obj['event'])

        if 'mac' in obj:
            o.setMacAddress(obj['mac'])
        else:
            o.setMacAddress(MacAddress([0, 0, 0, 0, 0, 0]))

        return o

    def add_neighbour(self, msg: Message):
        self.notify(msg)

    def remove_neighbour(self, msg: Message):
        self.notify(msg)

    def notify(self, msg: Message):
        log.info("Sending to {} '{}'".format(type(self._notifier).__name__, msg))
        self._notifier.on_notify(msg)

    def stop(self):
        log.info("Stopping server..")
        self.ip.release()
        self.serve = False

    def serve_forever(self):
        while self.serve:
            sleep(0.01)
