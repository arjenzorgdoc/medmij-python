from unittest import TestCase
from unittest.mock import patch, MagicMock
import lxml

import medmij
from . import testdata


def string_urlopen(s):
    cm = MagicMock()
    cm.getcode.return_value = 200
    cm.read.return_value = s
    cm.__enter__.return_value = cm
    return cm


class TestWhitelist(TestCase):
    def test_parse_ok(self):
        for xml in (testdata.whitelist_example_xml,
                    testdata.whitelist_example_single_xml):
            w = medmij.Whitelist(xml)
            self.assertTrue(isinstance(w, medmij.Whitelist))

    def test_parse_invalid_xml(self):
        with self.assertRaises(lxml.etree.XMLSyntaxError):
            medmij.Whitelist('<kapot')

    def test_parse_xsd_fail(self):
        for xml in (testdata.whitelist_xsd_fail1,
                    testdata.whitelist_xsd_fail2):
            with self.assertRaises(lxml.etree.XMLSyntaxError):
                medmij.Whitelist(xml)

    def test_whitelist_contains(self):
        whitelist = medmij.Whitelist(testdata.whitelist_example_xml)
        self.assertIn("rcf-rso.nl", whitelist)
        self.assertNotIn("rcf-rso.nl.", whitelist)
        self.assertNotIn("RFC-RSO.NL", whitelist)
        self.assertNotIn("", whitelist)
        self.assertNotIn(None, whitelist)

    @patch('urllib.request.urlopen')
    def test_whitelist_download(self, mock_urlopen):
        mock_urlopen.return_value = string_urlopen(
            testdata.whitelist_example_xml)
        url = "https://example.com/MedMij_Whitelist_example.xml"
        w = medmij.Whitelist.from_url(url)
        self.assertIsInstance(w, medmij.Whitelist)
