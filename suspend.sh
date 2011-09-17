#!/bin/sh

xscreensaver-command -lock
sleep 1
dbus-send --print-reply --system --dest=org.freedesktop.UPower /org/freedesktop/UPower org.freedesktop.UPower.Suspend

