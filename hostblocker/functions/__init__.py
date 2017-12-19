import re

# init regex for adblock
ADBLOCK_MATCH = re.compile(r'^\|\|.*\^$')
ADBLOCK_MATCH_3RD = re.compile(r'^\|\|.*\^\$third-party$')
ADBLOCK_MATCH_POP = re.compile(r'^\|\|.*\^\$popup$')
ADBLOCK_MATCH_DOC = re.compile(r'^\|\|.*\^\$document$')
ADBLOCK_MATCH_POP_3RD = re.compile(r'^\|\|.*\^\$popup,third-party$')
ADBLOCK_MATCH_DOC_POP = re.compile(r'^\|\|.*\^\$document,popup$')

# init regex for XML tags
XML_TAG_MATCH = re.compile(r'<[^>]*>')

# init regex for domain segment
DOMAIN_SEG_MATCH = re.compile(r'^(?!-)[_a-zA-Z\d-]{1,63}(?<!-)$')
DOMAIN_ALPHA = re.compile(r'[a-zA-Z]')

# init regez for IP addresses
IP = re.compile(r'^\d+.\d+.\d+.\d+$')
