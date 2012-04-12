Download Expat:
http://sourceforge.net/projects/expat/

Educational links:
http://wiki.python.org/moin/EscapingXml
http://docs.python.org/library/pyexpat.html

Revision 1
Program structure:
	Driver holds reference to input file, XMLParser and UMLGenerator.
	Input file is passed to XMLParser.
	XMLParser generates lists of the Classes, Attributes, and Relations (Functions).
	These lists are passed to UMLGenerator.
	UMLGenerator uses the input lists to generate an output XMI file describing the UML.
	XMI file is output to disk, to be opened by ArgoUML or another .xmi compliant program.