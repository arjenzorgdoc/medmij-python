import pkg_resources
from lxml import etree
import urllib.request


class Whitelist:
    NS = "xmlns://afsprakenstelsel.medmij.nl/whitelist/release2/"
    _parser = None

    @classmethod
    def get_xsd_parser(cls):
        if cls._parser is None:
            data = pkg_resources.resource_string(__name__, "whitelist.xsd")
            xsdxml = etree.XML(data)
            xsd = etree.XMLSchema(xsdxml)
            cls._parser = etree.XMLParser(schema=xsd)

        return cls._parser

    def __init__(self, xmldata):
        parser = self.get_xsd_parser()
        xml = etree.fromstring(xmldata, parser=parser)
        self._d = self._parse(xml)
        print(self._d)

    def __contains__(self, key):
        return key in self._d

    def _parse(self, xml):
        NSS = {'w': Whitelist.NS}
        return set(xml.xpath(f'//w:MedMijNode/text()', namespaces=NSS))

    @classmethod
    def from_url(cls, url):
        with urllib.request.urlopen(url) as response:
            xmldata = response.read()
        return cls(xmldata=xmldata)
