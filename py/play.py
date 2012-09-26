#!/usr/bin/env python3

import sys
import os
import play_daemon

def put(str) :
    print("[PLAY] %s" % str)

def main(argv) :

    if len(argv) >= 2 :
        if argv[1] == "kill" :
            if play_daemon.get_daemon_pid() :
                play_daemon.send_command(argv[1:])
            play_daemon.kill_daemon()
        else :
            if not play_daemon.get_daemon_pid() :
                put("Run play daemon.")
                play_daemon.run_daemon()
            else :
                put("Daemon already running.")
            s = play_daemon.send_command(argv[1:])
            put(s)
    else :
        if play_daemon.get_daemon_pid() :
            put("Daemon is running.")
        else :
            put("Daemon is not running.")

if __name__ == "__main__" :
    main(sys.argv)
