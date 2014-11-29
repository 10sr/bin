#!/usr/bin/env python3

import sys
import os
from glob import glob
from shlex import split as shsplit

from play_command import ControllerA
import play_daemon as playd

from play_prompt import PlayPrompt as Prompt

def main(argv):
    c = Controller()
    p = Prompt(c)
    while True:
        r = p.input()
        if len(r) == 0:
            continue
        if r[0] == "bye":
            print("Bye!")
            break
        elif r:
            c.cmd(r)
            print(c.status)

def file_realpath(s):
    if os.access(s, os.R_OK):
        return os.path.realpath(s)
    else:
        return s

def play_put(str):
    print("[PLAY] %s" % str)

def mainA(argv) :               # async

    if len(argv) >= 2:
        if argv[1] == "kill":
            playd.kill_daemon()
        else:
            if not playd.get_daemon_pid():
                play_put("Run play daemon.")
                playd.run_daemon()
            else:
                play_put("Daemon already running.")
            r = list(map(file_realpath, argv[1:]))
            s = playd.send_command(r)
            play_put(s)
    else:
        if playd.get_daemon_pid():
            play_put("Daemon is running.")
        else:
            play_put("Daemon is not running.")

if __name__ == "__main__":
    mainA(sys.argv)
