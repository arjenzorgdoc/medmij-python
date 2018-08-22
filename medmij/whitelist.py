import pkg_resources

class Whitelist:
    @staticmethod
    def get_xsd():
        return pkg_resources.resource_string(__name__, "whitelist.xsd")

    def __init__(self, xml):
        xsd = self.get_xsd()
        
        
