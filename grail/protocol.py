# -*- coding: utf-8 -*-

from Crypto.Cipher import AES


class GrailProtocol:
    VERSION_GRAIL = 1
    HASH_ALGORITHM = 'SHA1'
    HEADER = f"GRAIL VERSION;{VERSION_GRAIL}\rHASH ALGORITHM;{HASH_ALGORITHM}\n"

    @staticmethod
    def pack(cmd, size=15):
        end = "".join("\0" for _ in range(size - len(cmd)))
        cmd = cmd + end
        return cmd.encode()

    @staticmethod
    def un_puck(bytes_cmd):
        bytes_cmd = bytes_cmd.split(b'\0', 1)[0]
        bytes_cmd = bytes_cmd.decode()
        return bytes_cmd

    @staticmethod
    def create_new_grail(login, key):
        if len(key) > 16:
            print("PSWD Vere big")

        key = GrailProtocol.pack(key, 16)
        cipher = AES.new(key, AES.MODE_EAX)

        with open(login + ".grail", "wb") as grail:
            grail_protected, tag = cipher.encrypt_and_digest(GrailProtocol.HEADER.encode())

            [grail.write(x) for x in (cipher.nonce, tag, grail_protected)]

    @staticmethod
    def unlock_grail(login, key):
        if len(key) > 16:
            print("PSWD Vere big")

        key = GrailProtocol.pack(key, 16)

        with open(login + ".grail", "rb") as grail:
            nonce, tag, grail_extract = [grail.read(x) for x in (16, 16, -1)]

            cipher = AES.new(key, AES.MODE_EAX, nonce)
            pure_grail = cipher.decrypt_and_verify(grail_extract, tag)

            return pure_grail.decode()

    @staticmethod
    def parse_grail(grail):
        header, body = grail.split("\n")
        header = header.split("\r")

        for i, _ in enumerate(header):
            header[i] = header[i].split(";")

        return header, body