from datasrc import ADBLOCK_MATCH
from datasrc import ADBLOCK_MATCH_3RD
from datasrc import ADBLOCK_MATCH_POP
from datasrc import ADBLOCK_MATCH_DOC
from datasrc import ADBLOCK_MATCH_POP_3RD
from datasrc import ADBLOCK_MATCH_DOC_POP
from datasrc import XML_TAG_MATCH


def remove_comments(line: str) -> str:
    """
    Removes comments from a line (everything after a '#' character).

    :param line: the line.
    :return: the line without comments.
    """
    return line.split('#', 1)[0]


def remove_adblock_comments(line: str) -> str:
    """
    Removes AdBlock comments from a line (everything after a '!' character).

    :param line: the line.
    :return: the line without comments.
    """
    return line.split('!', 1)[0]


def remove_ip_local(line: str) -> str:
    """
    Removes localhost IP (127.0.0.1) from a line.

    :param line: the line.
    :return: the line without the localhost IP.
    """
    return remove_ip(line, '127.0.0.1')


def remove_ip_zero(line: str) -> str:
    """
    Removes zero IP (0.0.0.0) from a line.

    :param line: the line.
    :return: the line without the zero IP.
    """
    return remove_ip(line, '0.0.0.0')


def remove_ip(
        line: str,
        ip: str) -> str:
    """
    Removes an IP from a line.

    :param line: the line.
    :param ip: the IP.
    :return: the line without the IP.
    """
    return line.replace(ip, '', 1)


def remove_dot(line: str) -> str:
    """
    Removes a dot from the beginning of a line.

    :param line: the line.
    :return: the line without the beginning dot.
    """
    if line.startswith('.'):
        return line.replace('.', '', 1)
    else:
        return line


def remove_adblock_text(line: str) -> str:
    """
    Retrieves a domain from an AdBlock rule line.
    If the line does not match one of the ADBLOCK* formats, an empty line is returned.

    :param line: the rule line.
    :return: the domain obtained from the line (or an empty line).
    """
    if ADBLOCK_MATCH.match(line):
        return line[2:-1]
    elif ADBLOCK_MATCH_3RD.match(line):
        return line[2:-13]
    elif ADBLOCK_MATCH_POP.match(line):
        return line[2:-7]
    elif ADBLOCK_MATCH_DOC.match(line):
        return line[2:-10]
    elif ADBLOCK_MATCH_POP_3RD.match(line):
        return line[2:-19]
    elif ADBLOCK_MATCH_DOC_POP.match(line):
        return line[2:-16]
    else:
        return ''


def remove_xml_tags(line: str) -> str:
    """
    Removes XML tags from a line.

    :param line: the line.
    :return: the line without XML tags.
    """
    return XML_TAG_MATCH.sub('', line)


def trim(line: str) -> str:
    """
    Trims leading and trailing spaces.

    :param line: the line.
    :return: the line without leading and trailing spaces.
    """
    return line.strip()
