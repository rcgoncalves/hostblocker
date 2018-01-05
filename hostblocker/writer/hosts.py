import io
import logging
import os
from typing import List

from hostblocker.writer import APP_HEADER


IP_VAR = 'HOSTBLOCKER_HOSTS_IP'
IP = os.getenv(IP_VAR, '0.0.0.0')


def write(
        hosts_list: List[str],
        header: str,
        out: str) -> int:
    """
    Generates the hosts file from the hosts map.
    Entries with score above the given threshold are written to the output file.

    :param hosts_list: the hosts list.
    :param header: the header to prepend to the file.
    :param out: the path to the output file.
    :return: 0 if no error occurred; a value greater than 0 if there was an IO error.
    """
    result = 0
    try:
        with open(out, 'w') as file:
            file.write(APP_HEADER)
            if header:
                file.write('### BEGIN HostBlocker Header\n')
                result += write_header(header, file)
                file.write('### END HostBlocker Header\n')
            file.write('### BEGIN HostBlocker Block List\n')
            result += write_hosts_list(hosts_list, file)
            file.write('### END HostBlocker Block List\n')
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
    try:
        for host in hosts_list:
            file.write(IP + ' ' + host + '\n')
    except IOError:
        logging.exception('IO error writing hosts list')
        return 1
    return 0
