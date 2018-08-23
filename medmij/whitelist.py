"""
Defineert de class Whitelist
"""
import urllib.request
from typing import AnyStr, Set, Any
import pkg_resources
from lxml import etree

class Whitelist:
    """
    Een whitelist zoals beschreven op https://afsprakenstelsel.medmij.nl/

    """
    NS = "xmlns://afsprakenstelsel.medmij.nl/whitelist/release2/"
    _parser: etree.XMLParser

    @classmethod
    def _get_xsd_parser(cls) -> etree.XMLParser:
        if cls._parser is None:
            data = pkg_resources.resource_string(__name__, "whitelist.xsd")
            xsdxml = etree.XML(data)
            xsd = etree.XMLSchema(xsdxml)
            cls._parser = etree.XMLParser(schema=xsd)

        return cls._parser

    def __init__(self, xmldata: AnyStr) -> None:
        parser = self._get_xsd_parser()
        xml = etree.fromstring(xmldata, parser=parser)
        self._hostnames = self._parse(xml)

    def __contains__(self, key: Any) -> bool:
        return key in self._hostnames

    @staticmethod
    def _parse(xml: "etree._Element") -> Set[str]:
        nss = {'w': Whitelist.NS}
        return set(xml.xpath(f'//w:MedMijNode/text()', namespaces=nss))

    @classmethod
    def from_url(cls, url: str) -> Whitelist:
        """Initialiseert een Whitelist vanuit een URL. Downloadt de lijst, parset en valideert deze.
        """
        with urllib.request.urlopen(url) as response:
            xmldata = response.read()
        return cls(xmldata=xmldata)
