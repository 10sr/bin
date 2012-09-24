#!/usr/bin/env python3

import sys
import os
import play_command

def parse_input(s) :
    if s == "" :
        return

    s = s.strip(" ")

    ix = s.find(" ")
    if ix == -1 :
        return (s, "")
    else :
        cm = s[:ix]
        arg = s[ix+1:].lstrip(" ")
        return (cm, arg)

def prompt() :
    home = os.getenv("HOME")
    d = os.getcwd()
    if home != "" :
        d = d.replace(home, "~")

    try :
        s = input("PLAY %s $ " % d)
    except EOFError :
        s = "bye"
        print("")
    return s

def main(argv) :
    while True :
        s = prompt()
        r = parse_input(s)
        # print("cm : %s, arg : %s" % r)
        if r :
            try :
                f = play_command.commands[r[0]]
                f(r[1])
            except KeyError :
                print("%s: command not found." % r[0])

main(sys.argv)
