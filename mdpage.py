#!/usr/bin/python3

import os

def make_file_list():
    """Return list of md file without .md extension"""
    l = os.listdir()
    return (f for f, e in map(os.path.splitext, l) \
                if e == ".md" and os.path.isfile(f + e))

def is_updated(f):
    """Return True if html file is not exist or markdown file is newer than htmls"""
    return not os.path.isfile(f + ".html") or file_newer(f + ".md", f + ".html")

def file_newer(f1, f2):
    """Return True if f1 is newer than f2"""
    return os.path.getmtime(f1) > os.path.getmtime(f2)

def main():
    for f in make_file_list():
        print(f)
        if is_updated(f):
            print("%s updated." % f)

main()
