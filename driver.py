__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import xml.sax
from xml_parser import XMLParser


def main():
    source = open('sample.xml')
    parser = XMLParser()
    xml.sax.parse(source, parser)
    print parser.generated

main()