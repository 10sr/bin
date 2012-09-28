#!/usr/bin/env python3
# http://d.hatena.ne.jp/rintaromasuda/20060725/1153780824

import sys, os, errno
import signal as sig
import socket
from pickle import dumps, loads

from mpg123 import MPG123A
from play_command import ControllerA

CONFIG_DIR = os.path.expanduser("~/.playd")
PIPE = CONFIG_DIR + "/daemon_sok"
P_PIPE = CONFIG_DIR + "/player_pipe"
PIDFILE = CONFIG_DIR + "/pid"
P_PIDFILE = CONFIG_DIR + "/player_pid"
BUFSIZE = 1024

def send_command(args) :
    """func for client program"""
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print('Connecting %s.' % repr(PIPE))
    s.connect(PIPE)
    t = dumps(args)
    if len(t) > BUFSIZE :
        print("Too large data!")
    elif len(t) == 0 :
        print("No data!")
    else :
        print("Sending:" + str(t))
        s.send(t)
        data = s.recv(1024).decode()
        print('Received:' + data)
    print('Closing.')
    s.close()
    return data

def get_player_pid() :
    return get_pid(P_PIDFILE)

def get_daemon_pid() :
    return get_pid(PIDFILE)

def get_pid(file) :
    try :
        f = open(file, "r")
        pid = int(f.read())
        f.close()
        os.getsid(pid)
        return pid
    except OSError as e :
        if e.errno == errno.ENOENT :
            # no PIDFILE
            return 0
        elif e.errno == errno.ESRCH :
            # no process
            return 0
        else :
            raise
    except IOError as e :
        if e.errno == errno.ENOENT :
            # no pidfile
            return 0

def kill_daemon() :
    pid = get_player_pid()
    if pid :
        os.kill(pid, sig.SIGTERM)
        print("Player killed.")
    pid = get_daemon_pid()
    if pid :
        os.kill(pid, sig.SIGTERM)
        print("Daemon killed.")
    clean_file()

def clean_file() :
    if not get_daemon_pid :
        try :
            os.remove(PIDFILE)
        except OSError as e :
            if e.errno == errno.ENOENT :
                pass
            else :
                raise
    try :
        os.remove(PIPE)
    except OSError as e :
        if e.errno == errno.ENOENT :
            pass
        else :
            raise

def run_daemon() :
    os.makedirs(CONFIG_DIR, exist_ok = True)

    if get_daemon_pid() :
        print("Daemon is already running. Now restart daemon.")
        kill_daemon()
    clean_file()

    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try :
        pid = os.fork()
        if pid > 0:
            # exit first parent
            # sys.exit(0)
            os.waitpid(pid, 0)
            return
    except OSError as e :
        print("fork #1 failed: %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/")   #don't prevent unmounting....
    os.setsid()
    os.umask(0)

    # do second fork
    try :
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            #print "Daemon PID %d" % pid
            open(PIDFILE, 'w').write("%d" % pid)
            sys.exit(0)
    except OSError as e :
        print("fork #2 failed: %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1)

    # start the daemon main loop
    daemon_main()

#################################################
# For internal

def daemon_main() :
    c = ControllerA(P_PIPE, P_PIDFILE)
    daemon_loop(c)
    exit(0)

def daemon_loop(c) :
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(PIPE)
    s.listen(1)
    conn, addr = s.accept()
    while True:
        data = conn.recv(BUFSIZE)
        if len(data) != 0 : # remote is not closed
            # ans = handle_command(player, loads(data))
            c.cmd(loads(data))
            ans = c.status
            if ans == None :
                break
            if ans == "" :
                ans = "Something wrong!"
            # do not send empty byte
            conn.send(ans.encode())
        else :
            ans = "Client closed?"
        conn.close()
        conn, addr = s.accept()
    conn.close()
    os.unlink(PIPE)
    return
