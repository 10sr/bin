#!/bin/sh

dir=.

dmenu_dir(){
    ls -1 --color=never "$1" | dmenu
}

get_file(){
    if test -f $1
    then
        xdg-open $1
    else
        get_file "$1/$(dmenu_dir $1)"
    fi
}

get_file ~/
