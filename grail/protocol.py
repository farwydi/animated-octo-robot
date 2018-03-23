# -*- coding: utf-8 -*-
import hashlib
from io import BytesIO
from os.path import join, exists
from struct import unpack, pack

from Cryptodome.Cipher import AES


class GrailException(Exception):
    """
    Std Grail exception class.
    """


class GrailProtocol(object):
    VERSION_GRAIL = 3
    HASH_ALGORITHM = 'sha1'

    def __init__(self, path=""):
        self.__path = path

    def return_path(self, login: str):
        return join(self.__path, (login + ".grail"))

    @staticmethod
    def gen_password_key(password: str):
        return hashlib.sha256(password.encode("utf-8")).digest()

    def check(self, login: str, password: str):
        if not exists(self.return_path(login)):
            return False

        with open(self.return_path(login), "rb") as grail:
            nonce, tag, grail_extract = [grail.read(x) for x in (16, 16, -1)]

            cipher = AES.new(self.gen_password_key(password), AES.MODE_EAX, nonce)
            try:
                cipher.decrypt_and_verify(grail_extract, tag)
            except ValueError:
                return False

            return True

    def open(self, login: str, key: bytes):
        """

        :param key:
        :param login:
        :return:
        :rtype (str, bytes, list)
        """
        with open(self.return_path(login), "rb") as grail:
            nonce, tag, grail_extract = [grail.read(x) for x in (16, 16, -1)]

            cipher = AES.new(key, AES.MODE_EAX, nonce)
            pure_grail = cipher.decrypt_and_verify(grail_extract, tag)

            with BytesIO(pure_grail) as grail:
                version, = unpack('i', grail.read(4))

                if version != self.VERSION_GRAIL:
                    raise GrailException("Unknown version of Grail protocol")

                len_header, = unpack('i', grail.read(4))
                algorithm = grail.read(len_header).decode("ascii")

                header_hash = hashlib.new(algorithm, version.to_bytes((version.bit_length() + 7) // 8, 'big'))
                header_hash.update(algorithm.encode('utf-8'))

                hash_size, = unpack('i', grail.read(4))
                block_chain = []
                len_block, = unpack('i', grail.read(4))

                for _ in range(len_block):
                    len_record, = unpack('i', grail.read(4))
                    record = grail.read(len_record)
                    chain = grail.read(hash_size)

                    block_chain.append((record, chain))

                return algorithm, header_hash.digest(), block_chain

        raise GrailException()

    def create(self, login: str, key: bytes, algorithm=None, block_chain=None):
        """

        :param key:
        :param login:
        :param algorithm:
        :param block_chain:
        :return:
        """
        if algorithm is None:
            algorithm = self.HASH_ALGORITHM

        if block_chain is None:
            block_chain = []

        grail_data = bytes()
        grail_data += pack("i", self.VERSION_GRAIL)
        grail_data += pack("i", len(algorithm))
        grail_data += algorithm.encode("ascii")
        grail_data += pack("i", hashlib.new(algorithm).digest_size)
        grail_data += pack("i", len(block_chain))

        for record, chain in block_chain:
            grail_data += pack("i", len(record))
            grail_data += record
            grail_data += chain

        cipher = AES.new(key, AES.MODE_EAX)

        with open(self.return_path(login), "wb") as grail:
            grail_protected, tag = cipher.encrypt_and_digest(grail_data)

            for wd in (cipher.nonce, tag, grail_protected):
                grail.write(wd)
