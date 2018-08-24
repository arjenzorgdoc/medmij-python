# pylint: skip-file
from typing import Any, AnyStr
from unittest import TestCase
from unittest.mock import patch, MagicMock
import lxml

import medmij
from . import testdata


def string_urlopen(response_string: AnyStr) -> Any:
    response = MagicMock()
    response.__enter__.return_value = response
    response.getcode.return_value = 200
    response.read.return_value = response_string
    return response


class TestWhitelist(TestCase):
    def test_parse_ok(self) -> None:
        for xml in (testdata.WHITELIST_EXAMPLE_XML,
                    testdata.WHITELIST_EXAMPLE_SINGLE_XML):
            whitelist = medmij.Whitelist(xml)
            self.assertTrue(isinstance(whitelist, medmij.Whitelist))

    def test_parse_invalid_xml(self) -> None:
        with self.assertRaises(lxml.etree.XMLSyntaxError):
            medmij.Whitelist('<kapot')

    def test_parse_xsd_fail(self) -> None:
        for xml in (testdata.WHITELIST_XSD_FAIL1,
                    testdata.WHITELIST_XSD_FAIL2):
            with self.assertRaises(lxml.etree.XMLSyntaxError):
                medmij.Whitelist(xml)

    def test_whitelist_contains(self) -> None:
        whitelist = medmij.Whitelist(testdata.WHITELIST_EXAMPLE_XML)
        self.assertIn("rcf-rso.nl", whitelist)
        self.assertNotIn("rcf-rso.nl.", whitelist)
        self.assertNotIn("RFC-RSO.NL", whitelist)
        self.assertNotIn(None, whitelist)

    def test_whitelist_download(self) -> None:
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value = string_urlopen(
                testdata.WHITELIST_EXAMPLE_XML)
            whitelist = medmij.Whitelist.from_url("http://example.com/")
        self.assertIsInstance(whitelist, medmij.Whitelist)
