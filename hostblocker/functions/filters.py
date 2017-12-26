import logging

from hostblocker.functions import DOMAIN_SEG_MATCH
from hostblocker.functions import DOMAIN_ALPHA


def is_not_blank(line: str) -> bool:
    """
    Checks if a line has no contents.

    :param line: the line.
    :return: True if the line has no contents; False otherwise.
    """
    return bool(line.strip())


def is_not_2nd_level_domain(domain: str) -> bool:
    """
    Checks if this is a second level domain.

    :param domain: the domain.
    :return: True if this is not a 2nd level domain; False otherwise.
    """
    return domain.count('.') > 1


def is_not_top_level_domain(domain: str) -> bool:
    """
    Checks if this is a top level domain.

    :param domain: the domain.
    :return: True if this is not a top level domain; False otherwise.
    """
    return domain.count('.') > 0


def is_valid_domain(domain: str) -> bool:
    """
    Checks if this is a valid domain.
    A valid domain must:
    * be shorter than 256 characters;
    * not start nor end with a dot;
    * contain letters;
    * have segments shorter than 64 characters;
    * have only chars '[_-a-zA-Z]' characters in each segment, and not start not end with '-'.

    :param domain: the domain.
    :return: True if this is a valid domain; False otherwise.
    """
    res = len(domain) < 256 \
        and not domain.startswith('.') and not domain.endswith('.') \
        and bool(DOMAIN_ALPHA.search(domain)) \
        and all(DOMAIN_SEG_MATCH.match(seg) for seg in domain.split("."))
    if not res:
        logging.warning('invalid domain %s', domain.encode('utf-8'))
    return res
