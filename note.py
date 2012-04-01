#!/usr/bin/python3

program = "pcmanfm"
dir = "~/dbx/note"
trash = "~/.backup/memo"

import os
import subprocess as sp
import sys
import fileinput
import itertools as it
import datetime

dir = os.path.expanduser(dir)
trash = os.path.expanduser(trash)

def print_list(dir, func):
    #list = filter(filter_trash, os.listdir(dir))
    #list = (f for f in os.listdir(dir) if f != trash)
    list = os.listdir(dir)
    i = 0
    for f in list:
        i = i + 1
        print("%2d : " % i, end = "")
        print(f)
    if(func):
        ask_open(dir, list, func)

# def nth(iterable, n, default=None):
#     "Returns the nth item or a default value"
#     return next(it.islice(iterable, n, None), default)

def ask_open(dir, list, func):
    s = input("Input num: ")
    if(s == ""):
        exit()
    else:
        func(dir, list[int(s) - 1])

def edit_file(dir, name):
    #path = os.path.join(dir, name)
    os.chdir(dir)
    os.access(name, os.F_OK) or os.mknod(name, 0o644)
    sp.call([program, name])

def cat_file(dir, name):
    os.chdir(dir)
    for l in fileinput.input(name):
        print(l, end = "")
    print("")

def remove_file(dir, name):
    cat_file(dir, name)
    time = datetime.datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
    s = input("Really remove %s? [y/N]: " % name)
    if(s == "y"):
        os.rename(os.path.join(dir, name),
                  os.path.join(trash, name + "." + time))

def print_help():
    b = os.path.basename(sys.argv[0])
    print("%s: usage: %s [e|c|l|rm] [file]" % (b, b))
    pass


os.makedirs(dir, 0o755, True)
os.makedirs(trash, 0o755, True)
if(len(sys.argv) == 3):
    if(sys.argv[1] == "e"):
        edit_file(dir, sys.argv[2])
    elif(sys.argv[1] == "c"):
        cat_file(dir, sys.argv[2])
    elif(sys.argv[1] == "rm"):
        remove_file(dir, sys.argv[2])
    else:
        print_help()
elif(len(sys.argv) == 2):
    if(sys.argv[1] == "e"):
        print_list(dir, edit_file)
    elif(sys.argv[1] == "c"):
        print_list(dir, cat_file)
    elif(sys.argv[1] == "rm"):
        print_list(dir, remove_file)
    elif(sys.argv[1] == "l"):
        print_list(dir, None)
    else:
        print_help()
else:
    print_list(dir, None)

