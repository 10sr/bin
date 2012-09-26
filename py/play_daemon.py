#!/usr/bin/env python3
# http://d.hatena.ne.jp/rintaromasuda/20060725/1153780824

import sys, os, errno
import signal as sig
import socket
from pickle import dumps, loads
from mpg123 import MPG123A

CONFIG_DIR = os.path.expanduser("~/.playd")
PIPE = CONFIG_DIR + "/socket"
PIDFILE = CONFIG_DIR + "/pid"
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

def handle_command(p, args) :
    print("Server:")
    if args[0] == "exit" :
        p.exit()
        return None
    elif args[0] == "play" :
        p.play()
    elif args[0] == "pp" :
        p.playpause()
    elif args[0] == "stop" :
        p.stop()
    elif args[0] == "add" :
        p.add(args[1:])
    elif args[0] == "up" :
        p.up()
    elif args[0] == "down" :
        p.down()
    elif args[0] == "kill" :
        p.p.kill()
    print("Server:" + p.status)
    return p.status

def get_daemon_pid() :
    """return pid of daemon if it is running, otherwise 0"""
    try :
        f = open(PIDFILE, "r")
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

def kill_daemon() :
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

def daemon_main() :
    m = MPG123A()
    daemon_loop(m)
    exit(0)

def daemon_loop(player) :
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(PIPE)
    s.listen(1)
    conn, addr = s.accept()
    while True:
        data = conn.recv(BUFSIZE)
        if len(data) != 0 : # remote is not closed
            ans = handle_command(player, loads(data))
            if ans == None :
                break
            if ans == "" :
                ans = "Something wrong!"
            # do not send empty byte
        else :
            ans = "Client closed?"
        conn.send(ans.encode())
        conn.close()
        conn, addr = s.accept()
    conn.close()
    os.unlink(PIPE)
    return

def run_daemon() :
    os.makedirs(CONFIG_DIR, exist_ok = True)

    if get_daemon_pid() :
        print("Daemon is already running. Restart daemon.")
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
