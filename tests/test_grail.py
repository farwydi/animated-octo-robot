import difflib
import os
import random
import string
import unittest

from grail import Grail


def cut(s1, s2):
    diff = []
    for i, _1 in enumerate(s1):
        if len(diff) == 0 or type(diff[-1]) != int:
            if _1 != s2[i]:
                diff.append(i)
        else:
            if _1 == s2[i]:
                diff.append((diff.pop(), i))

    if len(diff) > 0 and type(diff[-1]) == int:
        diff.append((diff.pop(), len(s1)))

    return diff


def vis(diff, s2):
    for t in diff:
        x, y = t

        print((x, y, s2[x:y]))


class TestProtocol(unittest.TestCase):
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

    def test_diff_1(self):
        s1 = "asddfgzxc123374"
        s2 = "asdasdzxc123345"
        diff = cut(s1, s2)
        vis(diff, s2)

    def test_diff_2(self):
        s1 = """I am the very model of a modern Major-General,
My animation's comical, unusual, and whimsical,
I know the kings of England, and I quote the fights historical,
From Marathon to Waterloo, in order categorical."""

        s2 = """I am the very model of a cartoon individual,
My animation's comical, unusual, and whimsical,
I'm quite adept at funny gags, comedic theory I have read,
From wicked puns and stupid jokes to anvils that drop on your head."""

        d = difflib.Differ()
        diff = d.compare(s1.splitlines(), s2.splitlines())
        print('\n'.join(diff))
