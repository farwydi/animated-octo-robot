import base64
import hashlib
import os

import diff_match_patch as dmp_module

from protocol import GrailProtocol as gp, GrailException


class Grail(object):
    def __init__(self):
        self.header = None
        self.body = []
        self._init = False
        self.login = None
        self.key = None
        self.prev_hash = None

    def _get_last_hash(self):
        return self.prev_hash.encode("ascii")

    def insert(self, raw_str_diff):
        """
        Добавляет в конец grail новую запись.

        Новый хэш равен сумме предыдущий хэш и хэш новой записи.
        :param raw_str_diff:
        :return:
        """
        if not self._init:
            raise GrailException("not init")

        # Создаём объект хэша на основе предыдущего.
        hash_prev = hashlib.sha1(self._get_last_hash())

        # Кодируем входную строку в base64 и дополняем хэш.
        encode_record = base64.b64encode(raw_str_diff.encode('utf-8'))
        hash_prev.update(encode_record)

        # Обновляем последний хэш.
        self.prev_hash = hash_prev.hexdigest()

        # Добавляем индексацию.
        self.body.append((encode_record.decode('ascii'), self.prev_hash))

    def create(self, login, key):
        if os.path.exists(login + ".grail"):
            raise GrailException("file exist")

        gp.create_new_grail(login, key)

        self.open(login, key)

    def open(self, login, key):
        if not os.path.exists(login + ".grail"):
            raise GrailException("file not find")

        self.header, self.body = gp.parse_grail(gp.unlock_grail(login, key))

        _, self.prev_hash = self.body.pop()

        self.login = login
        self.key = key

        self._init = True

    def valid(self):
        prev = hashlib.sha1(gp.pack_header(self.header).encode("ascii")).hexdigest()

        for record, b_hash in self.body:
            next_hash = hashlib.sha1()
            next_hash.update(prev.encode("ascii"))
            next_hash.update(record.encode("ascii"))

            prev = next_hash.hexdigest()

            if prev != b_hash:
                return False

        return True

    def update(self, new_grail):
        if not self._init:
            raise GrailException("not init")

        if not self.valid():
            raise GrailException("no valid")

        dmp = dmp_module.diff_match_patch()

        patch = dmp.patch_make(self.get(), new_grail)

        self.insert(dmp.patch_toText(patch))

    def get(self):
        if not self._init:
            raise GrailException("not init")

        dmp = dmp_module.diff_match_patch()

        patches = []
        for base64_diff, _ in self.body:
            patches.append(dmp.patch_fromText(base64.b64decode(base64_diff).decode('ascii')))

        grail = ''
        for patch in patches:
            grail = dmp.patch_apply(patch, grail)[0]

        return grail

    def save(self, force=True):
        if not self._init:
            raise GrailException("not init")

        if force and os.path.exists(self.login + ".grail"):
            os.unlink(self.login + ".grail")

        gp.create_new_grail(self.login, self.key, gp.pack_header(self.header), self.body)
