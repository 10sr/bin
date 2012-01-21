#!/bin/bash
# todo : examine what happens about simlink and enable archive().

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
date_num=`date +%Y%m%d-%H%M%S`
returncode=0
message=""

notify(){                       # gnome notify first argument
    exec 10> >(zenity --notification --listen --window-icon "/usr/share/pixmaps/gnome-set-time.png")
    echo "visible: false" >&10
    echo "message: $1" >&10
    sleep 1
    exec 10>&-
}

archive(){                      # $ archive dir
    dir="$dst"
    files="$(find $(echo ${dir}/*) -maxdepth 0 '!' -name newest -type d)"
    arc="`format ${dir}/${pack_out} ${date_num}`"
    test `echo $files | wc -w` -gt 100 &&
    ${pack_cmd} "${arc}" ${files} &&
    echo rm -rf ${files}
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
        rsync -avh --stats --delete --backup --backup-dir=../${date_num} $fromdir $todir
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

notify "$message"
exit $returncode
