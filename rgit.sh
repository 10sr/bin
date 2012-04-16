#!/bin/bash

src="$HOME/.xdg-dirs/Dropbox/"
dst="$HOME/.backup/Dropbox_git/"
log="${dst}/rgit.log"

export DISPLAY=:0.0
export LANG=ja_JP.UTF-8
export LC_TIME=C
export GIT_DIR=$dst/rep
export GIT_WORK_TREE=.

header=$(printf "\nrgit $src > $dst: run at "; date;)
returncode=0
message=""
mkdir -p "$dst"

git_ci(){
    echo "$header"
    cd $src
    test -d $dst/rep || git init
    git add -v -A .
    if test -n "`git status -s -uno`"
    then
        git commit -m "$0 commit"
    else
        return 0
    fi
}

{
    git_ci
    returncode=$?
} | tee -a $log

if test $returncode -eq 0
then
    message="Commit done successfully."
else
    message="!!! Commit failed. Check log."
fi

if type notify-send >/dev/null 2>&1
then
    notify-send "rgit.sh" "$message"
fi

exit $returncode
