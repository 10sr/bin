#!/bin/bash
# 0 * * * * bash r.sh Dropbox

if test -z "$1"
then
    echo "usage: $0 srcdir" 1>&2
    exit 1
fi

src="$1"
dst="$HOME/.my/Dropbox"
log="${dst}/cronrsync.log"
errorlog="${dst}/cronrsyncerror.log"
pack_cmd="7z a"
pack_out="%s.7z"

export LANG=ja_JP.UTF-8
export LC_TIME=C

fromdir="$src/"        # must end with "/"
todir="$dst/newest/"

ctime=`date +%Y%m%d-%H%M%S`
returncode=0
message=""
archivemsg=""

archive_bak(){                      # $ archive dir
    dir="${dst}/"
    files="$(find $(echo ${dir}/*) -maxdepth 0 '!' -name newest -type d)"
    arc="`printf ${dir}/${pack_out} ${ctime}`"
    if test `echo $files | wc -w` -gt 150
    then
        if echo "Start packing backup files" &&
            ${pack_cmd} "${arc}" ${files} &&
            rm -rf ${files}
        then
            archivemsg="Archiving backup files successfully."
            return 0
        else
            archivemsg="!!! Tried to archive backup files but failed!"
            return 1
        fi
    fi
}

notify(){
    if type notify-send >/dev/null 2>&1
    then
        export DISPLAY=:0.0
        notify-send "r.sh" "$1"
    elif type growlnotify >/dev/null 2>&1
    then
        growlnotify -m "$1" -t "r.sh"
    fi
}

log_header(){
    local header=$(printf "\nCRON rsync $fromdir > $todir: run at "; date;)
    echo "$header" >>$log
    echo "$header" >>$errorlog
}

message_error(){
    test -z "$1" && return
    echo "$1" >>$errorlog
    echo "$1" 1>&2
    notify "$1"
}

message_normal(){
    test -z "$1" && return
    echo "$1" >> $log
    echo "$1"
    notify "$1"
}

log_header

if ! test -d "$fromdir"
then
    message_error "r.sh: $fromdir: Directory not found."
    exit 1
fi

size_fromdir=$(du -s "$fromdir" | cut -f 1)

if [ "$size_fromdir" -lt 1000 ]; then  # size is less than 1MB
    message="Size of $fromdir is less than 1MB, so did not back up in case files are unexpectedly lost."
    message_error "$message"
    returncode=1
else
    mkdir -p $todir
    {
        rsync -avh --stats --delete --backup --backup-dir=../${ctime} $fromdir $todir
    } >>$log 2>>$errorlog
    returncode=$?
    if [ $returncode -eq 0 ]; then
        message="rsync $fromdir > $todir: Done successfully."
        message_normal "$message"
    else
        message="!!! rsync $fromdir > $todir: Something wrong happened!"
        message_error "$message"
    fi
fi

if archive_bak >>$log 2>>$errorlog
then
    message_normal "$archivemsg"
else
    message_error "$archivemsg"
fi

exit $returncode
