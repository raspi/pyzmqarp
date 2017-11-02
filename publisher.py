#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

log = logging.getLogger(__name__)

import sys
from lib.notifiers.zmq import ZMQNotifier

from lib.arp import ArpNetworkNeighborNotifier


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s: %(message)s",
    )

    notifier = ZMQNotifier()
    notifier.listen()

    arpnotify = ArpNetworkNeighborNotifier()
    arpnotify.setNotifier(notifier)
    arpnotify.initlisten()
    arpnotify.serve_forever()
