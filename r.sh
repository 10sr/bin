#!/bin/bash

fromdir="$HOME/Dropbox/"        # must end with "/"
todir="$HOME/bu/dropbox/"
log="$HOME/bu/tb/cronrsync.log"
errorlog="$HOME/bu/tb/cronrsyncerror.log"

export DISPLAY=:0.0
export LANG=ja_JP.UTF-8
export LC_TIME=C

size_fromdir=$(du -s "$fromdir" | awk '{print $1}')
header=$(printf "\nCRON rsync $fromdir > $todir: run at "; date;)
returncode=0
message=""

notify(){                       # gnome notify first argument
    exec 10> >(zenity --notification --listen --window-icon "/usr/share/pixmaps/gnome-set-time.png")
    echo "visible: false" >&10
    echo "message: $1" >&10
    sleep 1
    exec 10>&-
}

# mkdir -p $todir || {
#     message="rsync $fromdir > $todir: Target dir is not writable."
#     {
#         echo "$header"
#         echo "$message"
#     } >>$errorlog
#     notify "$message"
#     exit 1
# }

if [ "$size_fromdir" -lt 1000 ]; then  # size is less than 1MB
    message="Size of $fromdir is less than 1MB, so did not back up in case files are unexpectedly lost."
    {
        echo "$header"
        echo "$message"
    } >>$errorlog
    echo "$message" 1>&2
    returncode=1
else
    {
        echo "$header"
        rsync -avh --stats --delete $fromdir $todir
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
