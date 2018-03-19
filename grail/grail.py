import base64
import os

from protocol import GrailProtocol as GP, GrailException


class Grail(object):
    def __init__(self):
        self.header = None
        self.body = []
        self._init = False
        self.login = None
        self.key = None

    def insert(self, raw_str):
        if not self._init:
            raise GrailException("not init")

        encode = base64.b64encode(raw_str.encode('utf-8'))
        self.body.append(encode.decode('ascii'))

    def create(self, login, key):
        if os.path.exists(login + ".grail"):
            raise GrailException("file exist")

        GP.create_new_grail(login, key)

        self.open(login, key)

    def open(self, login, key):
        if not os.path.exists(login + ".grail"):
            raise GrailException("file not find")

        self.header, self.body = GP.parse_grail(GP.unlock_grail(login, key))

        self.login = login
        self.key = key
        self._init = True

    def save(self):
        if not self._init:
            raise GrailException("not init")

        if os.path.exists(self.login + ".grail"):
            os.unlink(self.login + ".grail")

        GP.create_new_grail(self.login, self.key, GP.pack_header(self.header), self.body)
