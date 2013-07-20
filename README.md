pystrogram
==========

Display time-series histograms of Apache-style log files on the command-line.


Installation
------------

`pystogram` is a Python program and can be installed with `pip` or `easy_install`:

    $ pip install pystogram


Usage
-----

`pystogram` is a UNIX filter, so you can pass file names on the command line:

    $ pystogram /var/log/access.log

or pipe (possibly filtered) log data:

    $ grep lolcat /var/log/access.log | pystogram
