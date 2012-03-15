
import xml.parsers.expat

def start_element(name, attrs):
    print 'Start element:', name, attrs

def end_element(name):
    print 'End element:', name

def char_data(data):
    print 'Character data:', repr(data)

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

p = xml.parsers.expat.ParserCreate()

f = open('sample.xml')
r = f.read()

p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

parsed_data = p.Parse(r, 1)

print type(parsed_data)

for key, value in parsed_data:
    if key == 'Character Data':
        parsed_data['Character Data'] = unescape(value)

print parsed_data

