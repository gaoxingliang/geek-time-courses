#!/usr/bin/env python

import getopt
import sys
from .util import log
from .util import scriptname
from .geektime import run
import re

_options = [
    'help',
    'version',
    'parse',
    'download',
    "user",
    "pass",
    "courseid"
]
_short_options = 'hvpdU:P:C:'

_help = """Usage: {} [OPTION] [URL]
URL:  some url like "https://time.geekbang.org/course/intro/175"  

Options:
-U/--user XXXX          : set the cellphone of geektime account
-P/--pass XXXX          : set the password of account
-h/--help               : show help
-p/--parse              : only parse and extract the url (not downloading, this is default)
-d/--download           : download the courses all videos


""".format("geektime.py")

def printHelp():
    print(_help)

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
        printHelp()
    else:
        conf = {}
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                # Display help.
                printHelp()

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
            elif opt in ("-d", "--download"):
                conf["download"] = True
        if not args:
            printHelp()
        else:
            match = re.search(r'https?://time.geekbang.org/course/intro/(\d+)', args[0])
            if match:
                conf["courseid"] = match.group(1)
                run(**conf)
            else:
                print("Not support url - ", args[0])
                printHelp()