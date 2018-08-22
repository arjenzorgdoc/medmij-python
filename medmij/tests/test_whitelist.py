from unittest import TestCase

import medmij

class TestWhitelist(TestCase):
    def test_can_parse(self):
        w = medmij.Whitelist("<xml/>")
        self.assertTrue(isinstance(w, medmij.Whitelist))
