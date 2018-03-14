#!/bin/bash

dir=.

args=("$@")

dmenu_dir(){
    ls -1 --color=never "$1" | dmenu "${args[@]}" -p "$1/"
}

get_file(){
    test -e "$1" || return 1

    if test -f "$1"
    then
        exec xdg-open "$1"
    else
        file="$(dmenu_dir "$1")"
        test -n "$file" || return 1
        if test "$file" == "."
        then
            exec xdg-open "$1"
        else
            get_file "$(realpath "$1/${file}")"
        fi
    fi
}

get_file ~
