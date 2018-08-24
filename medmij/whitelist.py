"""
Defineert de class Whitelist
"""
from __future__ import annotations
import urllib.request
from typing import AnyStr, Set, Optional
import pkg_resources
from lxml import etree

class Whitelist:
    """
    Een whitelist zoals beschreven op https://afsprakenstelsel.medmij.nl/
    """
    NS = "xmlns://afsprakenstelsel.medmij.nl/whitelist/release2/"
    _parser: Optional[etree.XMLParser] = None

    @classmethod
    def _get_xsd_parser(cls) -> etree.XMLParser:
        if cls._parser is None:
            data = pkg_resources.resource_string(__name__, "whitelist.xsd")
            xsdxml = etree.fromstring(data)
            xsd = etree.XMLSchema(xsdxml)
            cls._parser = etree.XMLParser(schema=xsd)

        return cls._parser

    def __init__(self, xmldata: AnyStr) -> None:
        parser = self._get_xsd_parser()
        xml = etree.fromstring(xmldata, parser=parser)
        self._hostnames = self._parse(xml)

    def __contains__(self, key: object) -> bool:
        return key in self._hostnames

    @staticmethod
    def _parse(xml: etree.Element) -> Set[str]:
        nss = {'w': Whitelist.NS}
        return set(xml.xpath(f'//w:MedMijNode/text()', namespaces=nss))

    @classmethod
    def from_url(cls, url: str) -> Whitelist:
        """Initialiseert een Whitelist vanuit een URL. Downloadt de lijst, parset en valideert deze.
        """
        with urllib.request.urlopen(url) as response:
            xmldata = response.read()
        return cls(xmldata=xmldata)
