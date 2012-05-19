#!/usr/bin/python3

import os

def make_file_list():
    l = os.listdir()
    return (f for f, e in map(os.path.splitext, l) \
                if e == ".py" and os.path.isfile(f + e))

def is_md_file(f):
    e = os.path.splitext(f)[1]
    return e == ".py"

def main():
    for f in make_file_list():
        print(f)

main()
