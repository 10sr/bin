#!/bin/bash
set -e

# r2.sh --- Backup tool using rsync

# run every 00 min.
# 0 * * * * bash r2.sh Dropbox Dropbox_backup

##########################
# prefs
src="$1"
# dst="$HOME/.var/Dropbox_backup"
dst="$2"
pack_cmd="7z a"
pack_out="%s.7z"



########################

export LANG=ja_JP.UTF-8
export LC_TIME=C

ctime=`date +%Y%m%d-%H%M%S`
fromdir=
todir=
size_fromdir=

_logger="logger -i -t r2.sh"
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
    test -z "$1" && exit 1
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
    # here i want absolute path
    files="$(find "${dst}" -maxdepth 1 -name '????????-??????' -type d)"
    arc="`printf ${dir}/${pack_out} ${ctime}`"
    if test `echo $files | wc -w` -gt 150
    then
        echo  "Start packing backup files" | $logger_info
        if ${pack_cmd} "${arc}" ${files} &&
            rm -rf ${files}
        then
            msg "Archiving backup files successfully"
        else
            err "!!! Tried to archive backup files but failed!"
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
        err "!!! rsync $fromdir > $todir: " \
            "Something wrong happened!"
    fi
}

##############################
# main

test -z "$src" && err "src not specified"
test -z "$dst" && err "dst not specified"

fromdir="$src/"        # must end with "/"
todir="$dst/newest/"

echo "Now trying rsync $fromdir > $todir" | $logger_info

test -d "$fromdir" || err "$fromdir: Source directory not found"

size_fromdir=$(du -s "$fromdir" | cut -f 1)

if [ "$size_fromdir" -lt 1000 ]; then  # size is less than 1MB
    err "Size of $fromdir is less than 1MB, " \
        "abort in case files are unexpectedly lost"
else
    do_rsync
    do_archive_bak
fi
