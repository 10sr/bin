#!/usr/bin/python3

program = "pcmanfm"
notedir = "~/dbx/note"
trash = "~/.backup/memo"

import os
import subprocess as sp
import sys
import fileinput
import itertools as it
import datetime

notedir = os.path.expanduser(notedir)
trash = os.path.expanduser(trash)

def print_list(func):
    #list = filter(filter_trash, os.listdir(notedir))
    #list = (f for f in os.listdir(notedir) if f != trash)
    list = os.listdir(notedir)
    i = 0
    for f in list:
        i = i + 1
        print("%2d : " % i, end = "")
        print(f)
    if(func):
        ask_open(list, func)

# def nth(iterable, n, default=None):
#     "Returns the nth item or a default value"
#     return next(it.islice(iterable, n, None), default)

def ask_open(list, func):
    s = input("Input num: ")
    if(s == ""):
        exit()
    else:
        func(list[int(s) - 1])

def edit_file(name):
    #path = os.path.join(notedir, name)
    os.chdir(notedir)
    os.access(name, os.F_OK) or os.mknod(name, 0o644)
    sp.call([program, name])

def cat_file(name):
    os.chdir(notedir)
    for l in fileinput.input(name):
        print(l, end = "")
    print("")

def remove_file(name):
    cat_file(name)
    time = datetime.datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
    s = input("Really remove %s? [y/N]: " % name)
    if(s == "y"):
        os.rename(os.path.join(notedir, name),
                  os.path.join(trash, name + "." + time))

def print_help():
    b = os.path.basename(sys.argv[0])
    print("%s: usage: %s [e|c|l|rm] [file]" % (b, b))
    pass


os.makedirs(notedir, 0o755, True)
os.makedirs(trash, 0o755, True)
if(len(sys.argv) == 3):
    if(sys.argv[1] == "e"):
        edit_file(sys.argv[2])
    elif(sys.argv[1] == "c"):
        cat_file(sys.argv[2])
    elif(sys.argv[1] == "rm"):
        remove_file(sys.argv[2])
    else:
        print_help()
elif(len(sys.argv) == 2):
    if(sys.argv[1] == "e"):
        print_list(edit_file)
    elif(sys.argv[1] == "c"):
        print_list(cat_file)
    elif(sys.argv[1] == "rm"):
        print_list(remove_file)
    elif(sys.argv[1] == "l"):
        print_list(None)
    else:
        print_help()
else:
    print_list(None)

