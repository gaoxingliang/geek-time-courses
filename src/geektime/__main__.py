#!/usr/bin/env python

import getopt
import sys
from .util import log
from .util import scriptname
from .geektime import run

_options = [
    'help',
    'version',
    'parse',
    'download',
    "user",
    "pass",
    "course"
]
_short_options = 'hvpdU:P:C:'

_help = """Usage: {} [OPTION]... [URL]...
TODO
""".format("geektime.py")


def main():
    # Get options and arguments.
    try:
        opts, args = getopt.getopt(sys.argv[1:], _short_options, _options)
    except getopt.GetoptError as e:
        log.wtf("""
        [Fatal] {}.
        Try '{} --help' for more options.""".format(e, scriptname))

    if not opts and not args:
        # Display help.
        print(_help)
    else:
        conf = {}
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                # Display help.
                print(_help)

            elif opt in ('-v', '--version'):
                # Display version.
                log.println("{}", scriptname, log.BOLD)
            elif opt in ('-p', '--parse'):
                conf["parse"] = True
            elif opt in ('-U', '--user'):
                conf["user"] = arg
            elif opt in ('-P', '--pass'):
                conf["pass"] = arg
            elif opt in ("-C", "--courseid"):
                conf["courseid"] = arg

        run(**conf)
