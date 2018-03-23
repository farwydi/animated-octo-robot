import os
import random
import string
import tempfile
import unittest

from grail import Grail


def gen_random_string(N=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


class TestGrail(unittest.TestCase):

    def test_grail_2(self):
        # Получаем случайное имя для файла.
        login = next(tempfile._get_candidate_names())
        key = gen_random_string(16)

        text1 = """I am the very model of a modern Major-General,
My animation's comical, unusual, and whimsical,
I know the kings of England, and I quote the fights historical,
From Marathon to Waterloo, in order categorical."""

        text2 = """I am the very model of a cartoon individual,
My animation's comical, unusual, and whimsical,
I'm quite adept at funny gags, comedic theory I have read,
From wicked puns and stupid jokes to anvils that drop on your head."""

        g = Grail(tempfile.gettempdir())
        g.open(login, key)

        grail_file = g.get_grail_file()

        self.assertTrue(os.path.exists(grail_file))

        g.update(text1)
        g.update(text2)

        self.assertTrue(g.valid())

        self.assertEqual(g.get(), text2)

        g.save()
        g.open(login, key)

        self.assertEqual(g.get(), text2)

        g.destroy()

        # self.assertFalse(os.path.exists(grail_file))
