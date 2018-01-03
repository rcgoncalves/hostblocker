import io
import logging
from typing import DefaultDict, List

from hostblocker.writer import APP_HEADER


# Minimum number of domains with common suffix to replace with wildcard.
WILDCARD_MIN_DOMAINS = 3


def write(
        hosts: DefaultDict[str, int],
        header: str,
        out: str,
        threshold: int=1) -> int:
    """
    Generates the DNSMasq config file from the hosts map.
    Entries with score above the given threshold are written to the output file.

    :param hosts: the hosts map.
    :param header: the header to prepend to the file.
    :param out: the path to the output file.
    :param threshold: the score threshold (default: 1).
    :return: 0 if no error occurred; a value greater than 0 if there was an IO error.
    """
    result = 0
    hosts_list = {k for k, v in hosts.items() if v >= threshold}
    logging.info('score filter: %d/%d (threshold: %d)', len(hosts_list), len(hosts), threshold)
    hosts_list = sorted(hosts_list, key=reverse_domain)
    try:
        with open(out, 'w') as file:
            file.write('; ' + APP_HEADER)
            if header:
                file.write('; ### BEGIN HostBlocker Header\n')
                result += write_header(header, file)
                file.write('; ### END HostBlocker Header\n')
            file.write('; ### BEGIN HostBlocker Block List\n')
            result += write_hosts_list(hosts_list, file)
            file.write('; ### END HostBlocker Block List\n')
    except IOError:
        logging.exception('IO error writing hosts')
        result += 1
    return result


def write_header(
        header: str,
        file: io.TextIOWrapper) -> int:
    """
    Writes the header to the file.

    :param header: the path to the header file.
    :param file: the output file.
    :return: 0 if no error occurred; 1 if there was an IO error.
    """
    try:
        with open(header, 'r') as header_file:
            contents = header_file.read()
            file.write(contents)
            if not contents[-1].isspace():
                file.write('\n')
    except IOError:
        logging.exception('IO error writing header')
        return 1
    return 0


def write_hosts_list(
        hosts_list: List[str],
        file: io.TextIOWrapper) -> int:
    """
    Writes the list of hosts to a file.

    :param hosts_list: the list of hosts.
    :param file: the output file.
    :return: 0 if no error occurred; 1 if there was an IO error.
    """
    prev = '<invalid>'
    pending = []
    try:
        for host in hosts_list:
            if host.endswith(prev):
                pending.append(host)
            else:
                if len(pending) >= WILDCARD_MIN_DOMAINS:
                    # Replace pending with wildcard.
                    logging.info('use wildcard *.%s for %s', prev, str(pending))
                    file.write('*.' + prev + ' CNAME .\n')
                else:
                    # No wildcard replacement, so write pending hosts.
                    for pending_host in pending:
                        file.write(pending_host + ' CNAME .\n')
                pending = []
                prev = host
                file.write(host + ' CNAME .\n')
        if len(pending) >= WILDCARD_MIN_DOMAINS:
            # Replace pending with wildcard.
            logging.info('use wildcard *.%s for %s', prev, str(pending))
            file.write('*.' + prev + ' CNAME .\n')
        else:
            # No wildcard replacement, so write pending hosts.
            for pending_host in pending:
                file.write(pending_host + ' CNAME .\n')
    except IOError:
        logging.exception('IO error writing hosts list')
        return 1
    return 0


def reverse_domain(domain: str) -> str:
    """
    Reverses the segments of a domain name.

    :param domain: the domain to reverse.
    :return: the reversed domain.
    """
    return '.'.join(reversed(domain.split('.')))
