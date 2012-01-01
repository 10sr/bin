#!/bin/sh

usage(){
    echo "$0 UUID IP" 2>&1
}

start(){
    vboxmanage startvm $1 --type headless
}

connect(){
    while(! ping $1 -c 1 -W 1 >/dev/null 2>&1)
    do
        true
    done

    ssh $1
}

stop(){
    vboxmanage controlvm $1 savestate
}

if test $# -ne 2
then
    usage
    return 1
else
    start $1
    connect $2
    stop $1
fi
