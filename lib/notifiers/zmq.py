#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

log = logging.getLogger(__name__)

import sys
import json

from ipaddress import IPv4Address
from ipaddress import IPv6Address
from ipaddress import _BaseAddress

from lib.message import Message

from .notifier import Notifier

import zmq


class ZMQNotifier(Notifier):
    _ip = IPv4Address("127.0.0.1")
    _port = 5565
    _proto = "tcp"
    _sock = None

    def _getSockString(self):
        return "{0}://{1}:{2}".format(self._proto, self._ip, self._port)

    def setIP(self, ip: _BaseAddress):
        self._ip = ip

    def setPort(self, p:int):
        if not (p > 0 and p < 65535):
            raise ValueError("invalid range")
        self._port = p

    def listen(self):
        self.validate()
        log.info("Starting ZMQ Publisher..")
        self._sock = zmq.Context().socket(zmq.PUB)
        bindaddr = self._getSockString()
        log.info("Binding to '{}'".format(bindaddr))
        self._sock.bind(bindaddr)

    def stop(self):
        if self._sock is not None:
            log.info("Closing ZMQ socket..")
            self._sock.close()

    def on_notify(self, msg:Message):
        log.info("Received {} {}".format(sys._getframe().f_code.co_name, msg))
        self.send_to_wire(type(msg).__name__, json.dumps(msg.toObject(), sort_keys=True))

    def send_to_wire(self, topic, data):
        log.info("Sending to socket: '{}'".format(data))
        self._sock.send_string("{} {}".format(topic, data))

    def validate(self) -> bool:
        if not (isinstance(self._ip, IPv4Address) or isinstance(self._ip, IPv6Address)):
            raise TypeError("IP address is invalid")

        return True