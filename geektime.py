#!/usr/bin/env python3
import os, sys

_srcdir = '%s/src/' % os.path.dirname(os.path.realpath(__file__))
_filepath = os.path.dirname(sys.argv[0])
sys.path.insert(1, os.path.join(_filepath, _srcdir))

if sys.version_info[0] == 3:
    from src import geektime

    if __name__ == '__main__':
        geektime.main()
else:
    print("Not support python2")
