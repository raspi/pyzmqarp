#!/usr/bin/env python
# -*- coding:utf-8 -*-

from typing import List


class InvalidMacAddressException(ValueError):
    pass


IntList = List[int]


class MacAddress():
    _errors = []
    _mac = [-1, -1, -1, -1, -1, -1]

    def __repr__(self):
        return "{0}('{1}')".format(type(self).__name__, self.getstr())

    def __str__(self):
        return "{}".format(self.getstr())

    def __init__(self, mac):
        self._mac = self._convert(mac)

        if not self.validate():
            raise InvalidMacAddressException("\n".join(self._get_errors()))

    def _getmacstr(self) -> str:
        return ":".join(list(map(lambda x: hex(x)[2:].zfill(2), self._mac)))

    def _add_error(self, err) -> bool:
        self._errors.append(err)
        return True

    def _get_errors(self) -> list:
        return self._errors

    def _convert(self, mac) -> IntList:
        if isinstance(mac, str):
            for i in [":", "-", ]:
                if mac.find(i) != -1:
                    return list(map(lambda x: int(x, 16), mac.split(i)))
        elif isinstance(mac, list):
            return mac

        raise TypeError("Wrong type: {}".format(type(mac)))

    def validate(self):
        if self._mac is None:
            self._add_error(u"'None' given.")

        if isinstance(self._mac, list) and len(self._get_errors()) == 0:
            if len(self._mac) == 6:
                for i in self._mac:
                    if not isinstance(i, int):
                        self._add_error(u"Invalid value: {0}".format(i))

                    if not (i >= 0 or i <= 255):
                        self._add_error(u"Invalid value: {0}".format(i))
            else:
                self._add_error(u"invalid length: {0}.".format(len(self._mac)))

        else:
            self._add_error(u"'{0}' is not list.".format(type(self._mac)))

        if len(self._get_errors()) == 0:
            return True

        return False

    def get(self) -> list:
        return self._mac

    def getstr(self) -> str:
        return ":".join(list(map(lambda x: hex(x)[2:].zfill(2), self._mac)))
