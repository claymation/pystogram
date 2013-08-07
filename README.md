pystrogram
==========

Display time-series histograms of Apache-style log files on the command-line.


Example
-------

    $ pystogram /var/log/access.log
    2012-07-16 01  **                                                         1493
    2012-07-16 02  ***                                                        2819
    2012-07-16 03  *******                                                    5753
    2012-07-16 04  **********                                                 7721
    2012-07-16 05  *******************                                       14833
    2012-07-16 06  **************************                                19914
    2012-07-16 07  **********************************                        25626
    2012-07-16 08  *****************************************************     39901
    2012-07-16 09  *******************************************************   40943
    2012-07-16 10  *************************************************         36690
    2012-07-16 11  ********************************************              32967
    2012-07-16 12  **************************************                    28989


Usage
-----

Pass log file names on the command line:

    $ pystogram /var/log/access.log

or pipe in some (possibly filtered) log data:

    $ grep lolcat /var/log/access.log | pystogram


Installation
------------

`pystogram` is a Python program and can be installed with `pip` (or `easy_install`):

    $ pip install pystogram


Contributing
------------

`pystogram` is open-source software and your contributions are welcome.

Open an [issue](https://github.com/claymation/pystogram/issues) on GitHub to report a bug or suggest an enhancement,
or better yet, fork the repo and send a [pull request](https://github.com/claymation/pystogram/pulls).
