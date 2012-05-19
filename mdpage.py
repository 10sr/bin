#!/usr/bin/python3

import os

def make_file_list():
    l = os.listdir()
    return (f for f in l if is_md_file(f) and os.path.isfile(f))

def is_md_file(f):
    e = os.path.splitext(f)[1]
    return e == ".py"

def main():
    for f in make_file_list():
        print(f)

main()
