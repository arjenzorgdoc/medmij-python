from unittest import TestCase

import medmij
from . import testdata


class TestWhitelist(TestCase):
    def test_can_parse(self):
        for xml in (testdata.whitelist_example_xml,
                    testdata.whitelist_example_single_xml):
            w = medmij.Whitelist(xml)
            self.assertTrue(isinstance(w, medmij.Whitelist))
