#!/bin/sh

list(){
    cat /proc/partitions
    cat /proc/mounts
    ls /dev/disks/by-label
}

LANG=C

type df >/dev/null 2>&1 && {
    df -h 2>/dev/null | grep --color=never --invert-match ^none
}

