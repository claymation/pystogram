from setuptools import setup

setup(
    name = "pystogram",
    version = "0.2.0",
    description = "Display time-series histograms of Apache-style log files on the command-line",
    author = "Clay McClure",
    author_email = "clay@daemons.net",
    url = "https://github.com/claymation/pystogram",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Logging',
    ],
    packages = ['pystogram'],
    scripts = ['bin/pystogram'],
    tests_require = ['pytest'],
)
