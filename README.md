# HostBlocker: Domain Blocker File Builder

## About
*HostBlocker* is an application that builds lists to block known *problematic* domains (e.g., associated to Spam, malware, tracking).
It takes a configuration file with multiple lists of such domains, and builds a unified output file, with a configurable format (currently it supports `/etc/hosts`, Dnsmasq, Bind/RPZ and Unbound formats).
When using Bind output format, it can group multiple subdomains under a common wildcard domain, in case both the base domain and certain number of different subdomains are present.
For Unbound, subdomain of blocked domains are discarded, as blocking a domain automatically blocks a subdomain.  With Unbound format, SOA records are also generated (which allows to define the TTL for NXDOMAIN responses).
Moreover, it allows to specify a blacklist, a whitelist, and a custom header.

Each source list may have a different format.
Mapper and filter functions should be used to obtain the valid/desired domains from each list.
That is, for each line of a list, first a sequence of mapper functions is applied to obtain the domain from the line, and then a sequence of filter functions is applied to determine if the domain should be used or discarded.

Moreover, each list has associated a score, and only domains for which the sum of scores from the different lists is above a certain threshold are used.
This allows users to use less reliable lists, without risking blocking wrong domains (assigning a low score to the list, we make sure the domain is blocked only if it appears in other lists too).

This application caches the downloaded files for a configurable amount of time (60 hours by default), to avoid downloading the file too often.
The cache directory can be specified with the environment variable `HOSTBLOCKER_CACHE_PATH` (uses relative directory `cache` by default).


## Links
* [Downloads](https://github.com/rcgoncalves/hostblocker/releases/)
* [Changelog](https://github.com/rcgoncalves/hostblocker/blob/master/CHANGELOG.md)
* [Issues](https://github.com/rcgoncalves/hostblocker/issues)


## Usage
The application supports the following options:
- `-s`/`--source`: path to the YAML sources list.
- `-o`/`--output`: path to output file (default: `hosts`).
- `-f`/`--format`: output format (currently supports `hosts`, `dnsmasq`, `bind` and `unbound`; default: `hosts`)
- `-p`/`--header`: path to the header file.
- `-w`/`--whitlist`: path to the whitelist (domains that are never blocked).
- `-b`/`--blacklist`: path to the blacklist (additional domains to block).
- `-t`/`--threashold`: score threshold to block a domain (default: 0).
- `-c`/`--cache`: number of hours to cache files (default: 60).

Moreover, certain options can be controlled through environment variables:
- `HOSTBLOCKER_CACHE_PATH`: cache directory (default: `./cache`).
- `HOSTBLOCKER_HOSTS_IP`: the IP to use in hosts file (default: `0.0.0.0`)
- `HOSTBLOCKER_BIND_WILDCARD_MIN_DOMAINS`: minimum number of subdomains to use a wildcard with Bind.
- `HOSTBLOCKER_UNBOUND_ZONE_TYPE`: zone type to use with Unbound (default: `always_nxdomain`).
- `HOSTBLOCKER_SOA_*`: SOA record fields (currently SOA records are only generated for Unbound).


## Sources List
The source lists are defined in a YAML file, which contains the list of source URLs (and their properties), as well as the global mappers and filters.

### List of URLs
The list of URLs is defined by the entry `sources`, which should contain a list of source items.
Each source item must have the following entries:
- `url`: the URL of the source list (typically an HTTP(S) URL, but may also be a local file, if using the prefix `file://`).
- `score`: the score of the list.

Additionally, each item may have the following optional properties:
- `mappers`: the sequence of mappers to apply to each line of the file (the order is important!).
- `filters`: the sequence of filters to apply to each line of the file (the order only affects performance).
- `header`: the number of header lines the file contains, and that should be discarded.

### Global Mappers and Filters
Besides the mappers and filters specified for each source list, global mappers and filters (i.e., to apply to all lists) can also be specified with the top level entries `mappers` and `filters`.
These functions are applied after the functions specific to the source list.


## License
HostBlocker, a domain blocker file builder

Copyright (C) 2017-2025 Rui Carlos Gonçalves

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <[https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)>.
