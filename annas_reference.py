#
#import xml.parsers.expat
#
#def start_element(name, attrs):
#    print 'Start element:', name, attrs
#
#def end_element(name):
#    print 'End element:', name
#
#def char_data(data):
#    print 'Character data:', repr(data)
#
def unescape(s):
    want_unicode = False
    if isinstance(s, unicode):
        s = s.encode("utf-8")
        want_unicode = True
        # the rest of this assumes that `s` is UTF-8
        list = []

        # create and initialize a parser object
        p = xml.parsers.expat.ParserCreate("utf-8")
        p.buffer_text = True
        p.returns_unicode = want_unicode
        p.CharacterDataHandler = list.append

        # parse the data wrapped in a dummy element
        # (needed so the "document" is well-formed)
        p.Parse("<e>", 0)
        p.Parse(s, 0)
        p.Parse("</e>", 1)

        # join the extracted strings and return
        es = ""
        if want_unicode:
            es = u""
        return es.join(list)

#p = xml.parsers.expat.ParserCreate()
#
#f = open('sample.xml')
#r = f.read()
#
#p.StartElementHandler = start_element
#p.EndElementHandler = end_element
#p.CharacterDataHandler = char_data
#
#parsed_data = p.Parse(r, 1)


#for key, value in parsed_data:
#    if key == 'Character Data':
#        parsed_data['Character Data'] = unescape(value)






from xml.parsers import expat

xmlFile = "sample.xml"

#Define a class that will store the character data
class xmlText(object):
    def __init__ (self):
        self.textBuff = ""
    def CharacterData(self, data):
        data = data.strip()
        if data:
            data = data.encode('ascii')
            self.textBuff += data + "\n"

    def Parse(self, fName):
        xmlParser = expat.ParserCreate()
        xmlParser.CharacterDataHandler = self.CharacterData
        xmlParser.Parse(open(fName).read(), 1)

xText = xmlText()
xText.Parse(xmlFile)
print "Text from %s\n=" % xmlFile
print xText.textBuff




import xml.sax

xmlFile = "sample.xml"
xmlTag = "TOZE"

class tagHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.tags = {}
    def startElement(self,name, attr):
        name = name.encode('ascii')
        self.tags[name] = self.tags.get(name, 0) + 1
        print "Tag %s = %d" % (name, self.tags.get(name))

xmlparser = xml.sax.make_parser()

tHandler = tagHandler()

xmlparser.setContentHandler(tHandler)

xmlparser.parse(xmlFile)
tags = tHandler.tags
if tags.has_key(xmlTag):
    print "%s has %d <%s> nodes." % (xmlFile, tags[xmlTag], xmlTag)


import re
import xml.sax.handler

def xml2obj(src):
    """
    A simple function to converts XML data into native Python object.
    """

    non_id_char = re.compile('[^_0-9a-zA-Z]')
    def _name_mangle(name):
        return non_id_char.sub('_', name)

    class DataNode(object):
        def __init__(self):
            self._attrs = {}    # XML attributes and child elements
            self.data = None    # child text data
        def __len__(self):
            # treat single element as a list of 1
            return 1
        def __getitem__(self, key):
            if isinstance(key, basestring):
                return self._attrs.get(key,None)
            else:
                return [self][key]
        def __contains__(self, name):
            return self._attrs.has_key(name)
        def __nonzero__(self):
            return bool(self._attrs or self.data)
        def __getattr__(self, name):
            if name.startswith('__'):
                # need to do this for Python special methods???
                raise AttributeError(name)
            return self._attrs.get(name,None)
        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                # multiple attribute of the same name are represented by a list
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value
        def __str__(self):
            return self.data or ''
        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return u'{%s}' % ', '.join([u'%s:%s' % (k,repr(v)) for k,v in items])

    class TreeBuilder(xml.sax.handler.ContentHandler):
        def __init__(self):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []
        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            # xml attributes --> python attributes
            for k, v in attrs.items():
                self.current._add_xml_attr(_name_mangle(k), v)
        def endElement(self, name):
            text = ''.join(self.text_parts).strip()
            if text:
                self.current.data = text
            if self.current._attrs:
                obj = self.current
            else:
                # a text only node is simply represented by the string
                obj = text or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(_name_mangle(name), obj)
        def characters(self, content):
            self.text_parts.append(content)

    builder = TreeBuilder()
    if isinstance(src,basestring):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    return builder.root._attrs.values()[0]

xml2obj(open('sample.xml').read())

import sys, string
from xml.sax import handler, make_parser

class MySaxDocumentHandler(handler.ContentHandler):             # [1]
    def __init__(self, outfile):                                # [2]
        self.outfile = outfile
        self.level = 0
        self.inInterest = 0
        self.interestData = []
        self.interestList = []
    def get_interestList(self):
        return self.interestList
    def set_interestList(self, interestList):
        self.interestList = interestList
    def startDocument(self):                                    # [3]
        print "--------  Document Start --------"
    def endDocument(self):                                      # [4]
        print "--------  Document End --------"
    def startElement(self, name, attrs):                        # [5]
        self.level += 1
        self.printLevel()
        self.outfile.write('Element: %s\n' % name)
        self.level += 2
        for attrName in attrs.keys():                           # [6]
            self.printLevel()
            self.outfile.write('Attribute -- Name: %s  Value: %s\n' %\
                               (attrName, attrs.get(attrName)))
        self.level -= 2
        if name == 'interest':
            self.inInterest = 1
            self.interestData = []
    def endElement(self, name):                                 # [7]
        if name == 'interest':
            self.inInterest = 0
            interest = string.join(self.interestData)
            self.printLevel()
            self.outfile.write('Interest: ')
            self.outfile.write(interest)
            self.outfile.write('\n')
            self.interestList.append(interest)
        self.level -= 1
    def characters(self, chrs):                                 # [8]
        if self.inInterest:
            self.interestData.append(chrs)
    def printLevel(self):                                       # [9]
        for idx in range(self.level):
            self.outfile.write('  ')

def test(inFileName):
    outFile = sys.stdout
    # Create an instance of the Handler.
    handler = MySaxDocumentHandler(outFile)
    # Create an instance of the parser.
    parser = make_parser()
    # Set the content handler.
    parser.setContentHandler(handler)
    inFile = open(inFileName, 'r')
    # Start the parse.
    parser.parse(inFile)                                        # [10]
    # Alternatively, we could directly pass in the file name.
    #parser.parse(inFileName)
    inFile.close()
    # Print out a list of interests.
    interestList = handler.get_interestList()
    print 'Interests:'
    for interest in interestList:
        print '    %s' % (interest, )

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print 'usage: python test.py infile.xml'
        sys.exit(-1)
    test(args[0])

if __name__ == '__main__':
    main()