#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

log = logging.getLogger(__name__)

import sys
import json
import inspect
from copy import deepcopy
from ipaddress import ip_address
from typing import List

from lib.macaddress import MacAddress
from lib.enums.states import State
from lib.enums.eventtypes import EventType
from lib.message import Message

from lib import message

import zmq

MessageList = List[Message]

def get_classes() -> MessageList:
    c = []
    for name, obj in inspect.getmembers(message):
        if name.lower().find(u"Message".lower()) == -1:
            continue
        if inspect.isclass(obj) and not inspect.isbuiltin(obj) and object not in obj.__bases__:
            inst = obj()
            if isinstance(inst, message.Message):
                c.append(inst)

    return c


def main():
    classes = get_classes()

    connect_to = "tcp://127.0.0.1:5565"

    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)
    s.setsockopt(zmq.RCVBUF, 0)
    s.subscribe("IPv4Message")
    s.subscribe("IPv6Message")

    try:
        while True:
            raw = s.recv_string()

            if raw.find(" ") == -1:
                continue

            a = raw.split(" ", 1)
            del raw

            topic = a[0]
            data = json.loads(a[1])

            cls = None
            for c in classes:
                if type(c).__name__.lower() == topic.lower():
                    cls = deepcopy(c)
                    break

            if cls is None:
                break

            del topic

            cls.setAddress(ip_address(data['Address']))
            cls.setEventType(EventType(int(data['EventType'])))
            cls.setInterfaceIndex(int(data['InterfaceIndex']))
            cls.setInterfaceName(data['InterfaceName'])
            cls.setState(State(int(data['State'])))
            cls.setMacAddress(MacAddress(data['MacAddress']))

            log.debug("{}".format(cls))

            del cls

    except KeyboardInterrupt:
        pass
    print("Done.")

if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s: %(message)s",
    )

    main()