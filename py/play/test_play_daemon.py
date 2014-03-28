#!/usr/bin/env python3

import play_daemon as d

#d.kill_daemon()

if not d.get_daemon_pid():
    d.run_daemon()
else:
    print("Daemon is running.")

d.send_command(["dfe", "bb"])
