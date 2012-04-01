#!/usr/bin/python3

program = "pcmanfm"
dir = "~/dbx/note"

import os
import subprocess as sp
import sys
import fileinput

dir = os.path.expanduser(dir)

def print_list(dir, func):
    list = os.listdir(dir)
    i = 0
    for f in list:
        i = i + 1
        print("%2d : " % i, end = "")
        print(f)
    if(func):
        ask_open(dir, list, func)

def ask_open(dir, list, func):
    s = input("Input num: ")
    if(s == ""):
        exit()
    else:
        func(dir, list[int(s) - 1])

def edit_file(dir, name):
    #path = os.path.join(dir, name)
    os.chdir(dir)
    sp.call([program, name])

def cat_file(dir, name):
    os.chdir(dir)
    for l in fileinput.input(name):
        print(l, end = "")
    print("")

def print_help():
    pass

if(len(sys.argv) == 3):
    if(sys.argv[1] == "e"):
        edit_file(dir, sys.argv[2])
    elif(sys.argv[1] == "c"):
        cat_file(dir, sys.argv[2])
    else:
        print_help()
elif(len(sys.argv) == 2):
    if(sys.argv[1] == "e"):
        print_list(dir, edit_file)
    elif(sys.argv[1] == "c"):
        print_list(dir, cat_file)
    elif(sys.argv[1] == "l"):
        print_list(dir, None)
    else:
        print_help()
else:
    print_list(dir, None)

