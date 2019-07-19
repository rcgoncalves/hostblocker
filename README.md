# HostBlocker: Domain Blocker File Builder
*HostBlocker* is an application that builds lists to block known *problematic* domains (e.g., associated to Spam, malware, tracking).
It takes a configuration file with multiple lists of such domains, and builds a unified output file, with a configurable format (currently it supports `/etc/hosts`, Dnsmasq, Bind/RPZ and Unbound formats).
When using Bind output format, it can group multiple sub-domains under a common wildcard domain, in case both the base domain and certain number of different sub-domains are present.
For Unbound, sub-domain of blocked domains are discarded, as blocking a domain automatically blocks a sub-domain.  With Unbound format, SOA records are also generated (which allows to define the TTL for NXDOMAIN responses).
Moreover, it allows to specify a blacklists, a whitelist, and a custom header.

Each source list may have a different format.
Mapper and filter functions should be used to obtain the valid/desired domains from each list.
That is, for each line of a list, first a sequence of mapper functions is applied to obtain the domain from the line, and then a sequence of filter functions is applied to determine if the domain should be used or discarded.

Moreover, each list has associated a score, and only domains for which the sum of scores from the different lists is above a certain threshold are used.
This allows users to use less reliable lists, without risking blocking wrong domains (assigning a low score to the list, we make sure the domain is blocked only if it appears in other lists too).

This application caches the downloaded files for a configurable amount of time (60 hours by default), to avoid downloading the file to often.
The cache directory can be specified with the environment variable `HOSTBLOCKER_CACHE_PATH` (uses relative directory `cache` by default).


## Installation
To install this application simply run the command `python setup.py install`.
This will make the command `hostblocker` available.

This application requires Python 3, and the Python package `yaml`, `setuptools`, and `coverage`.


## Usage
The application supports the following options:
- `-s`/`--source`: path to the YAML sources list.
- `-o`/`--output`: path to output file (default: `hosts`).
- `-f`/`--format`: output format (currently supports `hosts`, `dnsmasq`, `bind` and `unbound`; default: `hosts`)
- `-p`/`--header`: path to the header file.
- `-w`/`--whitlist`: path to the whitelist (domains that are never blocked).
- `-b`/`--blacklist`: path to the black list (additional domains to block).
- `-t`/`--threashold`: score threshold to block a domain (default: 0).
- `-c`/`--cache`: number of hours to cache files (default: 60).

Moreover, certain options can be controlled through environment variables:
- `HOSTBLOCKER_CACHE_PATH`: cache directory (default: `./cache`).
- `HOSTBLOCKER_HOSTS_IP`: the IP to use in hosts file (default: `0.0.0.0`)
- `HOSTBLOCKER_BIND_WILDCARD_MIN_DOMAINS`: minimum number of sub-domains to use a wildcard with Bind.
- `HOSTBLOCKER_UNBOUND_ZONE_TYPE`: zone type to use with Unbound (default: `always_nxdomain`).
- `HOSTBLOCKER_SOA_*`: SOA record fields (currently SOA records are only generated for Unbound).


## Sources List
The source lists are defined in a YAML file, which contains the list of source URLs (and their properties), as well as the global mappers and filters.

### List of URLs
The list of URLs is defined by the entry `sources`, which should contain a list of source items.
Each source item must have the following entries:
- `url`: the URL of the source list (typically a HTTP(S) URL, but may also be a local file, if using the prefix `file://`).
- `score`: the score of the list.

Additionally, each item may have the following optional properties:
- `mappers`: the sequence of mappers to apply to each line of the file (the order is important!).
- `filters`: the sequence of filters to apply to each line of the file (the order only affects performance).
- `header`: the number of header lines the file contains, and that should be discarded.

### Global Mappers and Filters
Besides the mappers and filters specified for each source list, global mappers and filters (i.e., to apply to all lists) can also be specified with the top level entries `mappers` and `filters`.
These functions are applied after the functions specific to the source list.


## TODO
- Add support to `Last-Modified` HTTP header when using cache.
- Check if domains are still active.
- Improve source lists encoding support (namely, allow compressed files).


## Change Log
- 1.4.3 (2019-07-19)
  - Use safer method for reading configuration
- 1.4.2 (2018-03-23)
  - Use cached file if download fails
- 1.4.1 (2018-03-06)
  - Remove default source file
- 1.4 (2018-01-05)
  - Add support for Unbound
- 1.3.1 (2018-01-05)
  - Code refactoring
  - Change default score threshold to 0
  - Allow specification of IP for hosts file
  - Sort output by reverse domain
  - Set remote connections timeout to 10s
- 1.3 (2018-01-03)
  - Add support for Bind
- 1.2 (2017-12-23)
  - Code refactoring
  - Add support for Dnsmasq
- 1.1 (2017-12-11)
  - Improve AdBlock mapper
  - Add support for caching sources
- 1.0 (2017-12-10)
  - Initial version


## Author
Rui Carlos Gonçalves (rcgoncalves.pt@gmail.com)


## License
*HostBlocker* is free software, distributed under the terms of the GNU General
Public License as published by the Free Software Foundation, version 3 of the License (or any later version).
For more information, see the file LICENSE.
