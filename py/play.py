#!/usr/bin/env python3

import sys
import os
from glob import glob
from shlex import split as shsplit

from play_command import Controller
import play_daemon as playd

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

def put(str) :
    print("[PLAY] %s" % str)

def main2(argv) :

    if len(argv) >= 2 :
        if argv[1] == "kill" :
            if playd.get_daemon_pid() :
                playd.send_command(argv[1:])
            playd.kill_daemon()
        else :
            if not playd.get_daemon_pid() :
                put("Run play daemon.")
                playd.run_daemon()
            else :
                put("Daemon already running.")
            s = playd.send_command(argv[1:])
            put(s)
    else :
        if playd.get_daemon_pid() :
            put("Daemon is running.")
        else :
            put("Daemon is not running.")

if __name__ == "__main__" :
    main(sys.argv)
