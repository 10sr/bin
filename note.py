#!/usr/bin/python3

program = "pcmanfm"
dir = "~/dbx/note"

import os
import subprocess as sp
import sys
import fileinput

dir = os.path.expanduser(dir)

def print_list(dir, p):
    list = os.listdir(dir)
    i = 1
    for f in list:
        print("%2d : " % i, end = "")
        i = i + 1
        print(f)
    ask_open(dir, list, p)

def ask_open(dir, list, p):
    s = input("Input num or c: ")
    if(s == ""):
        exit()
    elif(s == "c"):
        num = int(input("Input num: "))
        cat_file(dir, list[num - 1])
    else:
        open_file(dir, list[int(s) - 1], p)
    

def open_file(dir, name, p):
    #path = os.path.join(dir, name)
    os.chdir(dir)
    sp.call([p, name])

def cat_file(dir, name):
    os.chdir(dir)
    for l in fileinput.input(name):
        print(l, end = "")
    print("")

if(len(sys.argv) == 3):
    if(sys.argv[1] == "e"):
        open_file(dir, sys.argv[2], program)
    elif(sys.argv[1] == "c"):
        cat_file(dir, sys.argv[2])
    else:
        print_list(dir, program)
else:
    print_list(dir, program)

