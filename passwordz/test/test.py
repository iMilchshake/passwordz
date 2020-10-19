from unittest import TestCase

import win32clipboard
from parameterized import parameterized

from passwordz.password_generation import password_generation as pg


class Test(TestCase):

    @parameterized.expand([
        ["Master123", "pwid1", 3, "ABCDEFG"],
        ["M4st§1!3", "__!", 16, "A§CD!F?"],
        ["m4st3r", "somePWid123_?!", 12, "abcdeABCDE!?352"],
    ])
    def test_generate_password_flex_same_as_normal(self, mskey, pwid, pwlen, chars):
        assert pg.generatePassword(mskey, pwid, pwlen, chars) == pg.generatePasswordFlex(mskey, pwid, pwlen, chars)

    @parameterized.expand([
        [""],
        ["abcABC"],
        ["aA!?§_323C"]
    ])
    def test_clipboard(self, inp):
        pg.saveToClipboard(inp)
        win32clipboard.OpenClipboard()
        assert win32clipboard.GetClipboardData() == inp
        win32clipboard.CloseClipboard()