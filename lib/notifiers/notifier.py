#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

log = logging.getLogger(__name__)

import signal

from lib.message import Message


class Notifier():
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        self.stop()
        signal.signal(signal.SIGTERM, signal.SIG_IGN)

    def on_notify(self, msg: Message):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
