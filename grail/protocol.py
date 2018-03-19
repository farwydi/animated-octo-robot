# -*- coding: utf-8 -*-
from Crypto.Cipher import AES


class GrailException(Exception):
    pass


class GrailProtocol(object):
    VERSION_GRAIL = '2'
    HASH_ALGORITHM = 'SHA1'
    HEADER = f"VERSION;{VERSION_GRAIL}\nALGORITHM;{HASH_ALGORITHM}"

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
    def create_new_grail(login, key, header=HEADER, body=list()):
        if len(key) > 16:
            raise GrailException("password vere big")

        key = GrailProtocol.pack(key, 16)
        cipher = AES.new(key, AES.MODE_EAX)

        with open(login + ".grail", "wb") as grail:
            raw = header + "\n\n" + "\n".join(body)

            grail_protected, tag = cipher.encrypt_and_digest(raw.encode())

            for wd in (cipher.nonce, tag, grail_protected):
                grail.write(wd)

    @staticmethod
    def unlock_grail(login, key):
        if len(key) > 16:
            raise GrailException("password vere big")

        key = GrailProtocol.pack(key, 16)

        with open(login + ".grail", "rb") as grail:
            nonce, tag, grail_extract = [grail.read(x) for x in (16, 16, -1)]

            cipher = AES.new(key, AES.MODE_EAX, nonce)
            pure_grail = cipher.decrypt_and_verify(grail_extract, tag)

            return pure_grail.decode()

    @staticmethod
    def parse_grail(grail):
        header_raw, body = grail.split("\n\n")
        header = dict()
        for h_r in header_raw.split("\n"):
            hh = h_r.split(";")
            header.update({hh[0]: hh[1]})

        return header, body.split("\n")

    @staticmethod
    def pack_header(header):
        return f"VERSION;{header['VERSION']}\nALGORITHM;{header['ALGORITHM']}"
