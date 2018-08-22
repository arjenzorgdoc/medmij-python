import pkg_resources
from lxml import etree


class Whitelist:
    _xsd = None

    @classmethod
    def get_xsd(cls):
        if cls._xsd is None:
            data = pkg_resources.resource_string(__name__, "whitelist.xsd")
            cls._xsd = etree.XML(data)
        return cls._xsd

    def __init__(self, xmldata):
        xsd = self.get_xsd()
        xml = etree.XML(xmldata)
