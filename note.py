#!/usr/bin/python3

program = "leafpad"
notepath = "~/dbx/note"

import os
import subprocess as sp
import sys
import fileinput
import datetime

notepath = os.path.expanduser(notepath)
trash = ".trash"

def print_list(func):
    flist = [f for f in os.listdir(notepath) \
                 if f != trash and not f.endswith(".html")]
    i = 0
    for f in flist:
        i = i + 1
        print("%2d : %s" % (i, f))
    if func :
        ask_open(flist, func)

def ask_open(flist, func):
    s = input("Input num: ")
    if s == "":
        exit()
    else:
        func(flist[int(s) - 1])

def edit_file(filename):
    os.chdir(notepath)
    os.access(filename, os.F_OK) or os.mknod(filename, 0o644)
    sp.call([program, filename])

def cat_file(filename):
    for l in fileinput.input(os.path.join(notepath, filename)):
        print(l, end = "")
    print("")

def remove_file(filename):
    cat_file(filename)
    time = datetime.datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
    s = input("Really remove %s? [y/N]: " % filename)
    if s == "y" :
        os.rename(os.path.join(notepath, filename),
                  os.path.join(notepath, trash, filename + "." + time))

def print_help():
    b = os.path.basename(sys.argv[0])
    print("Usage: %s [e|c|rm] [file]" % b, file=sys.stderr)
    print("       %s l" % b, file=sys.stderr)
    exit(1)

def main():
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

os.access(os.path.join(notepath, trash), os.W_OK) or \
os.makedirs(os.path.join(notepath, trash), 0o755)

main()
