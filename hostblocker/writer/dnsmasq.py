import logging

from typing import TextIO

from hostblocker.writer import APP_HEADER


def write(
        hosts_list: list[str],
        header: str,
        out: str) -> int:
    """
    Generates the DNSMasq config file from the hosts map.
    Entries with score above the given threshold are written to the output file.

    :param hosts_list: the hosts list.
    :param header: the header to prepend to the file.
    :param out: the path to the output file.
    :return: 0 if no error occurred; a value greater than 0 if there was an IO error.
    """
    result = 0
    try:
        with open(out, 'w', encoding='utf-8') as file:
            file.write(APP_HEADER)
            if header:
                file.write('### BEGIN HostBlocker Header\n')
                result += write_header(header, file)
                file.write('### END HostBlocker Header\n')
            file.write('### BEGIN HostBlocker Block List\n')
            result += write_hosts_list(hosts_list, file)
            file.write('### END HostBlocker Block List\n')
    except OSError:
        logging.exception('IO error writing hosts')
        result += 1
    return result


def write_header(
        header: str,
        file: TextIO) -> int:
    """
    Writes the header to the file.

    :param header: the path to the header file.
    :param file: the output file.
    :return: 0 if no error occurred; 1 if there was an IO error.
    """
    try:
        with open(header, encoding='utf-8') as header_file:
            contents = header_file.read()
            file.write(contents)
            if not contents[-1].isspace():
                file.write('\n')
    except OSError:
        logging.exception('IO error writing header')
        return 1
    return 0


def write_hosts_list(
        hosts_list: list[str],
        file: TextIO) -> int:
    """
    Writes the list of hosts to a file.

    :param hosts_list: the list of hosts.
    :param file: the output file.
    :return: 0 if no error occurred; 1 if there was an IO error.
    """
    try:
        for host in hosts_list:
            file.write(f'server=/{host}/\n')
    except OSError:
        logging.exception('IO error writing hosts list')
        return 1
    return 0
