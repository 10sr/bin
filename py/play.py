#!/usr/bin/env python3

import sys
import os
from play_command import Controller
from glob import glob
from shlex import split as shsplit

def parse_input(s) :
    args = shsplit(s)
    eargs = [args[0]]
    for a in args[1:] :
        g = glob(a)
        if len(g) == 0 :
            eargs.extend([a])
        else :
            eargs.extend(g)
    return eargs

def prompt() :
    home = os.getenv("HOME")
    d = os.getcwd()
    if home != "" :
        d = d.replace(home, "~")

    try :
        s = input("PLAY %s $ " % d)
    except (EOFError, KeyboardInterrupt) :
        s = "bye"
        print("")
    return s

def main(argv) :
    c = Controller()
    while True :
        s = prompt()
        r = parse_input(s)
        if r[0] == "bye" :
            print("Bye!")
            break
        elif r :
            c.cmd(r)
            print(c.status)
            # try :
            #     f = play_command.commands[r[0]]
            #     f(r)
            # except KeyError :
            #     print("%s: command not found." % r[0])

main(sys.argv)
