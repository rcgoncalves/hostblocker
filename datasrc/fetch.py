import urllib.request
from typing import List


def get_lines(url: str) -> List[bytearray]:
    """
    Retrieves the lines of a URL.

    :param url: the URL.
    :return: the list of lines.
    """
    req = urllib.request.Request(url,
                                 data=None,
                                 headers={
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13)'
                                                  ' AppleWebKit/604.4.7 (KHTML, like Gecko)'
                                                  ' Version/11.0.2 Safari/604.4.7'
                                 })
    data = urllib.request.urlopen(req)
    return data.readlines()
