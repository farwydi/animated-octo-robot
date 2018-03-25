import hashlib
import os.path
import random
import string
import unittest
import tempfile
from protocol import GrailProtocol, GrailException


def gen_random_string(N=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


class TestProtocol(unittest.TestCase):

    def test_check_file_not_find(self):
        protocol = GrailProtocol()

        self.assertFalse(protocol.check("file not find", ""))

        with self.assertRaises(FileNotFoundError):
            protocol.read("file not find", b"")

    # def test_pack(self):
    #     # Проверка упаковки команды.
    #     test_cmd_len = 15
    #     for c in range(test_cmd_len + 1):
    #         self.assertEqual(len(GrailProtocol.pack(cmd="0" * c, size=test_cmd_len)), test_cmd_len)
    #
    # def test_un_pack(self):
    #     # Проверка распаковки команды.
    #     test_cmd_len = 15
    #     commands_true = ["0" * x for x in range(test_cmd_len + 1)]
    #     commands = [(b"\x30" * x) + b"\0" * (test_cmd_len - x) for x in range(test_cmd_len + 1)]
    #     for i, b_cmd in enumerate(commands):
    #         self.assertEqual(GrailProtocol.un_pack(b_cmd), commands_true[i])
    #
    # def test_grail(self):
    #     # Получаем случайное имя для файла.
    #     login = next(tempfile._get_candidate_names())
    #
    #     # Ключ не может быть больше 16 символов.
    #     key = gen_random_string(25)
    #     with self.assertRaises(GrailException):
    #         GrailProtocol.create_new_grail(login, key)
    #     with self.assertRaises(GrailException):
    #         GrailProtocol.unlock_grail("", key)
    #
    #     key = gen_random_string(16)
    #
    #     # Попытка создать файл.
    #     GrailProtocol.create_new_grail(login, key)
    #     self.assertTrue(os.path.exists(login + ".grail"))
    #
    #     # Попытка декодировать файл.
    #     r = GrailProtocol.unlock_grail(login, key)
    #     hash_prev = hashlib.sha1()
    #     hash_prev.update(GrailProtocol.HEADER.encode("ascii"))
    #     self.assertEqual(r, GrailProtocol.HEADER + "\n\n;" + hash_prev.hexdigest())
    #
    #     # Проверка целостности файла.
    #     r_header, r_body = GrailProtocol.parse_grail(r)
    #     self.assertEqual(r_header['VERSION'], GrailProtocol.VERSION_GRAIL)
    #     self.assertEqual(r_header['ALGORITHM'], GrailProtocol.HASH_ALGORITHM)
    #     self.assertEqual(r_body, [('', hash_prev.hexdigest())])
    #
    #     # Удаление временного файла.
    #     os.unlink(login + ".grail")


if __name__ == '__main__':
    unittest.main()
