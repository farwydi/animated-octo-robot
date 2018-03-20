import os
import random
import string
import unittest

import diff_match_patch as dmp_module

from grail import Grail


class TestGrail(unittest.TestCase):
    def test_grail(self):
        def gen_random_string(N=10):
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

        # Получаем случайное имя для файла.
        login = gen_random_string()
        while os.path.exists(login + ".grail"):
            login = gen_random_string()

        key = gen_random_string(16)

        g = Grail()
        g.create(login, key)
        g.insert(r"чвапвап\t\nasdsd")
        g.save()

        g = Grail()
        g.open(login, key)
        g.insert(r"чвапвап\t\nasdsd")
        g.save()

        g = Grail()
        g.open(login, key)

        os.unlink(login + ".grail")

    def test_grail_2(self):
        def gen_random_string(N=10):
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

        # Получаем случайное имя для файла.
        login = gen_random_string()
        while os.path.exists(login + ".grail"):
            login = gen_random_string()

        key = gen_random_string(16)

        text1 = """I am the very model of a modern Major-General,
My animation's comical, unusual, and whimsical,
I know the kings of England, and I quote the fights historical,
From Marathon to Waterloo, in order categorical."""

        text2 = """I am the very model of a cartoon individual,
My animation's comical, unusual, and whimsical,
I'm quite adept at funny gags, comedic theory I have read,
From wicked puns and stupid jokes to anvils that drop on your head."""

        g = Grail()
        g.create(login, key)

        self.assertTrue(os.path.exists(login + ".grail"))

        g.update(text1)
        g.update(text2)

        self.assertTrue(g.valid())

        self.assertEqual(g.get(), text2)

        os.unlink(login + ".grail")
