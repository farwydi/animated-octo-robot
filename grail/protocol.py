# -*- coding: utf-8 -*-
import hashlib

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
            hash_prev = hashlib.sha1()
            hash_prev.update(header.encode("ascii"))

            raw_body = GrailProtocol.pack_body(body)
            raw_body = "\n" + raw_body if len(raw_body) > 0 else ""

            raw = header + "\n\n" + ";" + hash_prev.hexdigest() + raw_body

            grail_protected, tag = cipher.encrypt_and_digest(raw.encode("ascii"))

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
