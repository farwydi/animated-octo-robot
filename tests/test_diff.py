import unittest
import base64
import diff_match_patch as dmp_module


class TestDiff(unittest.TestCase):

    def test_diff(self):
        text1 = """I am the very model of a modern Major-General,
My animation's comical, unusual, and whimsical,
I know the kings of England, and I quote the fights historical,
From Marathon to Waterloo, in order categorical."""

        text2 = """I am the very model of a cartoon individual,
My animation's comical, unusual, and whimsical,
I'm quite adept at funny gags, comedic theory I have read,
From wicked puns and stupid jokes to anvils that drop on your head."""

        dmp = dmp_module.diff_match_patch()

        patch = dmp.patch_make(text1, text2)

        raw_patch = dmp.patch_toText(patch)

        encode = base64.b64encode(raw_patch.encode('utf-8'))

        decode = base64.b64decode(encode)

        de_raw_str = decode.decode('ascii')

        re_patch = dmp.patch_fromText(de_raw_str)

        re_text2 = dmp.patch_apply(re_patch, text1)[0]

        self.assertEqual(re_text2, text2)
