#!/bin/sh

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

list_running(){
    echo "Running :"
    vbm list runningvms
    echo
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
    true
}

if test $# -eq 0
then
    list vms
elif test "$1" == start
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
else
    list "$@"
fi
