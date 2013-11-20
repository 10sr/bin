#!/bin/bash
set -e
# 0 * * * * bash r2.sh Dropbox

# use fd by exec

if test -z "$1"
then
    echo "usage: $0 <srcdir>" 1>&2
    exit 1
fi

##########################
# prefs
src="$1"
dst="$HOME/.var/Dropbox_backup"
pack_cmd="7z a"
pack_out="%s.7z"


########################

export LANG=ja_JP.UTF-8
export LC_TIME=C

fromdir="$src/"        # must end with "/"
todir="$dst/newest/"

ctime=`date +%Y%m%d-%H%M%S`
returncode=0

_logger="logger -i -t r.sh"
logger_info="$_logger -p 6"
logger_err="$_logger -p 3 -s"

################################
# utilities

notify(){
    # notify <msg> ...
    if type notify-send >/dev/null 2>&1
    then
        DISPLAY=:0.0 notify-send "r.sh" "$*"
    elif type growlnotify >/dev/null 2>&1
    then
        growlnotify -m "$*" -t "r.sh"
    fi
}

err(){
    test -z "$1" && return
    echo "$@" | $logger_err
    notify "$@"
    exit 1
}

msg(){
    test -z "$1" && return
    echo "$@" | $logger_info
    notify "$@"
}

##########################
# subroutines

do_archive_bak(){                      # $ archive dir
    dir="${dst}/"
    files="$(find $(echo ${dir}/*) -maxdepth 0 '!' -name newest -type d)"
    arc="`printf ${dir}/${pack_out} ${ctime}`"
    if test `echo $files | wc -w` -gt 150
    then
        msg "Start packing backup files"
        if ${pack_cmd} "${arc}" ${files} &&
            rm -rf ${files}
        then
            msg "Archiving backup files successfully"
            return 0
        else
            err "!!! Tried to archive backup files but failed!"
            return 1
        fi
    fi
}

do_rsync(){
    mkdir -p "$todir"
    rsync -avh --stats --delete --backup --backup-dir=../${ctime} \
        "$fromdir" "$todir" | $logger_info
    returncode=$?
    if [ $returncode -eq 0 ]; then
        msg "rsync $fromdir > $todir: Done successfully."
    else
        err "!!! rsync $fromdir > $todir: Something wrong happened! Check $stderr"
    fi
}

##############################
# main

echo "$fromdir > $todir" | $logger_info

if ! test -d "$fromdir"
then
    err "$fromdir: Directory not found"
fi

size_fromdir=$(du -s "$fromdir" | cut -f 1)

if [ "$size_fromdir" -lt 1000 ]; then  # size is less than 1MB
    err "Size of $fromdir is less than 1MB, " \
        "abort in case files are unexpectedly lost"
else
    do_rsync
    do_archive_bak
fi
