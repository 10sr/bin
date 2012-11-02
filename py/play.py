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

def file_realpath(s) :
    if os.access(s, os.R_OK) :
        return os.path.realpath(s)
    else :
        return s

def play_put(str) :
    print("[PLAY] %s" % str)

def mainA(argv) :               # async

    if len(argv) >= 2 :
        if argv[1] == "kill" :
            playd.kill_daemon()
        else :
            if not playd.get_daemon_pid() :
                play_put("Run play daemon.")
                playd.run_daemon()
            else :
                play_put("Daemon already running.")
            r = list(map(file_realpath, argv[1:]))
            s = playd.send_command(r)
            play_put(s)
    else :
        if playd.get_daemon_pid() :
            play_put("Daemon is running.")
        else :
            play_put("Daemon is not running.")

if __name__ == "__main__" :
    main(sys.argv)
