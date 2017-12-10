# HostBlocker: Host File Domain Blocker Builder

*HostBlocker* is an application that builds `/etc/hosts` files to block known *problematic* domains (e.g., associated to Spam, malware, tracking).
It takes a configuration file with multiple lists of such domains, and builds an unified file, with the expected format.
Moreover, it allows to specify an additional blacklists, a whitelist, and a custom header.

Each source list may have a different format.
Mapper and filter functions should be used to obtain the valid/desired domains from each list.
That is, for each line of a list, first a sequence of mapper functions is applied to obtain the domain from the line, and then a sequence of filter functions is applied to determine if the domain should be used or discarded.

Moreover, each list has associated a score, and only domains for which the sum of scores from the different lists is above a certain threshold are used.
This allows users to use less reliable lists, without risking blocking wrong domains (assigning a low score to the list, we make sure the domain is blocked only if it appears in other lists too).

## Installation

To install this application simply run the command `python setup.py install`.
This will make the command `hostblocker` available.

This application requires Python 3, and the Python package `yaml`. 

## Usage

The application supports the following options:
- `-s`/`--source`: path to the YAML sources list (default: `config/sources.yml`).
- `-o`/`--output`: path to output file (default: `hosts`).
- `-p`/`--header`: path to the header file.
- `-w`/`--whitlist`: path to the whitelist (domains that are never blocked).
- `-b`/`--blacklist`: path to the black list (additional domains to block).
- `-t`/`--threashold`: score threshold to block a domain (default: 4).


## Sources List

The source lists are defined in a YAML file, which contains the list of source URLs (and their properties), as well as the global mappers and filters.

### List of URLs
The list of URLs is defined by the entry `sources`, which should contain a list of source items.
Each source item must have the following entries:
- `url`: the URL of the source list (typically a HTTP(S) URL, but may also be a local file, if using the prefix `fil://`).
- `score`: the score of the list.

Additionally, each item may have the following optional properties:
- `mappers`: the sequence of mappers to apply to each line of the file (the order is important!).
- `filters`: the sequence of filters to apply to each line of the file (the order only affects performance).
- `header`: the number of header lines the file contains, and that should be discarded.


### Global Mappers and Filters
Besides the mappers and filters specified for each source list, global mappers and filters (i.e., to apply to all lists) can also be specified with the top level entries `mappers` and `filters`.
These functions are applied after the functions specific to the source list.

## TODO
- Cache downloaded files for a configurable period of time.
- Check if domains are still active.
- Support other output formats (support DNSMasq with wildcard domains).
- Improve source lists encoding support.

## Author
Rui Carlos Gonçalves <rcgoncalves.pt@gmail.com>

## License

*HostBlocker* is free software, distributed under the terms of the [GNU] General
Public License as published by the Free Software Foundation,
version 3 of the License (or any later version).  For more information,
see the file LICENSE.
