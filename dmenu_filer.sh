#!/bin/sh

dir=.

dmenu_dir(){
    ls -1 --color=never "$1" | dmenu -fn '-*-dejavu sans mono-*-r-*-*-11-*-*-*-*-*-*-*' -p "$1" -l 10 -i
}

get_file(){
    test -e $1 || return 1
    if test -f $1
    then
        exec xdg-open $1
    else
        file=$(dmenu_dir $1)
        test -n "$file" || return 1
        get_file "$1/${file}"
    fi
}

get_file ~
