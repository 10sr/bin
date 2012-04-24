#!/bin/bash

trap 'notify_exit; exit' 1 2 3 15

notify_setup(){
    exec 4> >(zenity --notification --listen --window-icon "/usr/share/pixmaps/gnome-set-time.png")
}

notify_display(){
    echo "message: $1" >&4
}

notify_exit(){
    exec 4>&-
}

if test -n "$1"; then
    zenity --info --title "count up timer" --text "exit?"
    kill $1
    exit 0
fi

min=0
bash $0 $$ &
notify_setup

while :; do
    sleep 10
    sleep 10
    sleep 10
    sleep 10
    sleep 10
    sleep 10
    min=$(expr ${min} + 1)
    notify_display "${min} minutes passed."
done

