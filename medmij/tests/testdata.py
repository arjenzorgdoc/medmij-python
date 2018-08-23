"""Testdata"""

import pkg_resources


def _load(name):
    return pkg_resources.resource_string(__name__, name)


WHITELIST_EXAMPLE_XML = _load("whitelist_example.xml")
WHITELIST_EXAMPLE_SINGLE_XML = _load("whitelist_example_single.xml")
WHITELIST_XSD_FAIL1 = "<test/>"
WHITELIST_XSD_FAIL2 = """<Whitelist
    xmlns="xmlns://afsprakenstelsel.medmij.nl/whitelist/release2/"
/>"""
