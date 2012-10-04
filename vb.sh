#!/bin/sh
# should i use vboxshell.py?

PATH="/ApplicationsVirtualBox.app/Contents/MacOS:$PATH"
if type VBoxManage >/dev/null 2>&1
then
    alias vbm=VBoxManage
elif type vboxmanage >/dev/null 2>&1
then
    alias vbm=vboxmanage
else
    echo "vboxmanage not exist!" 2>&1
    exit 127
fi

list(){
    vbm list "$@"
}

start(){
    if test -z "$1"
    then
        echo "Specify vm name to start!" 2>&1
        list vms
    else
        vbm startvm "$1" --type headless
    fi
}

gui(){
    if test -z "$1"
    then
        echo "Specify vm name to start!" 2>&1
        list vms
    else
        vbm startvm "$1" --type gui
    fi
}

suspend(){
    if test -z "$1"
    then
        echo "Specify vm name to suspend!" 2>&1
        list runningvms
    else
        vbm controlvm $1 savestate
    fi
}

help(){
    cmd="`basename $1`"
    echo "vb: $cmd [start|gui|suspend|vms|running|list]"
}

if test $# -eq 0
then
    echo VMS:
    list vms
    echo RUNNING:
    list runningvms
elif test "$1" == start
then
    start "$2"
elif test "$1" == gui
then
    start "$2"
elif test "$1" == suspend
then
    suspend "$2"
elif test "$1" == vms
then
    list vms
elif test "$1" == running
then
    list runningvms
elif test "$1" == list
then
    shift
    list "$@"
elif test "$1" == help
then
    help $0
else
    vbm "$@"
fi
