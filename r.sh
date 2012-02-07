#!/bin/bash

src="$HOME/.xdg-dirs/Dropbox/"
dst="$HOME/bu/Dropbox/"
log="$HOME/bu/tb/cronrsync.log"
errorlog="$HOME/bu/tb/cronrsyncerror.log"
pack_cmd="7z a"
pack_out="%s.7z"

export DISPLAY=:0.0
export LANG=ja_JP.UTF-8
export LC_TIME=C

fromdir="$src/"        # must end with "/"
todir="$dst/newest/"

size_fromdir=$(du -s "$fromdir" | awk '{print $1}')
header=$(printf "\nCRON rsync $fromdir > $todir: run at "; date;)
ctime=`date +%Y%m%d-%H%M%S`
returncode=0
message=""
archivemsg=""

notify(){                       # gnome notify first argument
    exec 5> >(zenity --notification --listen --window-icon "/usr/share/pixmaps/gnome-set-time.png")
    echo "visible: false" >&5
    echo "message: $1" >&5
    test -n "$2" && echo "message: $2" >&5
    sleep 1
    exec 5>&-
}

archive_bak(){                      # $ archive dir
    dir="$dst"
    files="$(find $(echo ${dir}/*) -maxdepth 0 '!' -name newest -type d)"
    arc="`printf ${dir}/${pack_out} ${ctime}`"
    if test `echo $files | wc -w` -gt 150
    then
        if echo "Start packing backup files" &&
            ${pack_cmd} "${arc}" ${files} &&
            rm -rf ${files}
        then
            archivemsg="Archiving backup files successfully."
            echo $archivemsg
            return 0
        else
            archivemsg="!!! Tried to archive backup files but failed!"
            echo $archivemsg 1>&2
            return 1
        fi
    fi
}

if [ "$size_fromdir" -lt 1000 ]; then  # size is less than 1MB
    message="Size of $fromdir is less than 1MB, so did not back up in case files are unexpectedly lost."
    {
        echo "$header"
        echo "$message"
    } >>$errorlog
    echo "$message" 1>&2
    returncode=1
else
    mkdir -p $todir
    {
        echo "$header"
        rsync -avh --stats --delete --backup --backup-dir=../${ctime} $fromdir $todir
    } >>$log 2>>$errorlog
    returncode=$?
    if [ $returncode -eq 0 ]; then
        message="rsync $fromdir > $todir: Done successfully."
        echo "$message"
    else
        message="!!! rsync $fromdir > $todir: Something wrong happened!"
        echo "$message" 1>&2
    fi
fi

if archive_bak >>$log 2>>$errorlog
then
    test -n "$archivemsg" && echo "$archivemsg"
else
    test -n "$archivemsg" && echo "$archivemsg" 1>&2
fi

notify "$message" "$archivemsg"
exit $returncode
