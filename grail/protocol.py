# -*- coding: utf-8 -*-
import hashlib
import io
import os.path
from struct import unpack, pack

from Cryptodome.Cipher import AES


class GrailException(Exception):
    """
    Std Grail exception class.
    """


class GrailProtocol(object):
    VERSION_GRAIL = 3
    HASH_ALGORITHM = 'sha1'
    HEADER = f"VERSION;{VERSION_GRAIL}\nALGORITHM;{HASH_ALGORITHM}"

    def __init__(self, path=""):
        self.__path = path
        self.__cipher = None
        self.__login = ""
        self.__init = False

    def return_path(self, login: str):
        return os.path.join(self.__path, (login + ".grail"))

    def open(self, login: str, key: str):
        key = hashlib.sha256(key.encode("utf-8")).digest()
        self.__cipher = AES.new(key, AES.MODE_EAX)

        with open(self.return_path(login), "rb") as grail:
            nonce, tag, grail_extract = [grail.read(x) for x in (16, 16, -1)]

            cipher = AES.new(key, AES.MODE_EAX, nonce)
            pure_grail = cipher.decrypt_and_verify(grail_extract, tag)

            with io.BytesIO(pure_grail) as grail:
                version, = unpack('i', grail.read(4))

                if version != self.VERSION_GRAIL:
                    raise GrailException("Unknown version of Grail protocol")

                len_header, = unpack('i', grail.read(4))
                algorithm = grail.read(len_header).decode("ascii")

                header_hash = hashlib.new(algorithm, version.to_bytes((version.bit_length() + 7) // 8, 'big'))
                header_hash.update(algorithm.encode('utf-8'))

                hash_size = header_hash.digest_size
                block_chain = []
                len_block, = unpack('i', grail.read(4))

                for _ in range(len_block):
                    len_record, = unpack('i', grail.read(4))
                    record = grail.read(len_record)
                    chain = grail.read(hash_size)

                    block_chain.append((record, chain))

                self.__login = login
                self.__init = True

                return algorithm, header_hash.digest(), block_chain

    def save(self, force=True):
        if self.__init and self.__cipher is not None:
            if force and os.path.exists(self.return_path(self.__login)):
                os.unlink(self.return_path(self.__login))

    def create(self, login: str, key: str, algorithm, block_chain=list()):
        key = hashlib.sha256(key.encode("utf-8")).digest()
        self.__cipher = AES.new(key, AES.MODE_EAX)

        grail_data = bytes()
        grail_data += pack("i", self.VERSION_GRAIL)
        grail_data += pack("i", len(algorithm))
        grail_data += self.HASH_ALGORITHM.encode("ascii")
        grail_data += pack("i", 0)

        with open(self.return_path(login), "wb") as grail:
            grail_protected, tag = self.__cipher.encrypt_and_digest(grail_data)

            for wd in (self.__cipher.nonce, tag, grail_protected):
                grail.write(wd)

    @staticmethod
    def pack(cmd, size=15):
        end = "".join("\0" for _ in range(size - len(cmd)))
        cmd = cmd + end
        return cmd.encode()

    @staticmethod
    def un_pack(bytes_cmd):
        bytes_cmd = bytes_cmd.split(b'\0', 1)[0]
        bytes_cmd = bytes_cmd.decode()
        return bytes_cmd

    @staticmethod
    def create_new_grail(login, key, header=HEADER, body=list(), path=""):
        if len(key) > 16 and len(key) > 0:
            raise GrailException("Password can not be longer than 16 characters or empty")

        key = GrailProtocol.pack(key, 16)
        cipher = AES.new(key, AES.MODE_EAX)

        with open(os.path.join(path, (login + ".grail")), "wb") as grail:
            hash_prev = hashlib.sha1()
            hash_prev.update(header.encode("ascii"))

            raw_body = GrailProtocol.pack_body(body)
            raw_body = "\n" + raw_body if len(raw_body) > 0 else ""

            raw = header + "\n\n" + ";" + hash_prev.hexdigest() + raw_body

            grail_protected, tag = cipher.encrypt_and_digest(raw.encode("ascii"))

            for wd in (cipher.nonce, tag, grail_protected):
                grail.write(wd)

    @staticmethod
    def unlock_grail(login, key, path=""):
        if len(key) > 16:
            raise GrailException("password vere big")

        key = GrailProtocol.pack(key, 16)

        with open(os.path.join(path, (login + ".grail")), "rb") as grail:
            nonce, tag, grail_extract = [grail.read(x) for x in (16, 16, -1)]

            cipher = AES.new(key, AES.MODE_EAX, nonce)
            pure_grail = cipher.decrypt_and_verify(grail_extract, tag)

            return pure_grail.decode()

    @staticmethod
    def parse_grail(grail):
        header_raw, body = grail.split("\n\n")
        header = dict()
        for h_r in header_raw.split("\n"):
            title, value = h_r.split(";")
            header.update({title: value})

        body = body.split("\n")

        for i, b in enumerate(body):
            base64_diff, prev_hash = b.split(";")
            body[i] = (base64_diff, prev_hash)

        return header, body

    @staticmethod
    def pack_header(header):
        return f"VERSION;{header['VERSION']}\nALGORITHM;{header['ALGORITHM']}"

    @staticmethod
    def pack_body(body):
        for i, b in enumerate(body):
            base64_diff, prev_hash = b
            body[i] = base64_diff + ";" + prev_hash

        return "\n".join(body)
