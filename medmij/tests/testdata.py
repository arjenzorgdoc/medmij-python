import pkg_resources


def _load(name):
    return pkg_resources.resource_string(__name__, name)


whitelist_example_xml = _load("whitelist_example.xml")
whitelist_example_single_xml = _load("whitelist_example_single.xml")
