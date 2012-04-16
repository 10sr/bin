#!/bin/bash

src="$HOME/.xdg-dirs/Dropbox/"
dst="$HOME/.backup/Dropbox_git/"
log="${dst}/cronrsync.log"

export DISPLAY=:0.0
export LANG=ja_JP.UTF-8
export LC_TIME=C

#fromdir="$src/"        # must end with "/"
#todir="$dst/"

header=$(printf "\nCRON rsync $fromdir > $todir: run at "; date;)
returncode=0
message=""
mkdir -p "$dst"

rsync_run(){
    echo "$header"
    rsync -avh --stats --delete "$fromdir" "$todir" 2>&1
}

export GIT_DIR=$dst/rep
export GIT_WORK_TREE=$src
git_ci(){
    cd $src
    test -d $dst/rep || git init
    git add -A *
    test -n "`git status -s`" && git commit -m "$0 commit"
}

git_ci

#rsync_run | tee -a "$log"
#returncode=$?

# if [ $returncode -eq 0 ]; then
#     message="rsync $fromdir > $todir: Done successfully."
#     echo "$message"
#     git_ci
# else
#     message="!!! rsync $fromdir > $todir: Something wrong happened!"
#     echo "$message" 1>&2
# fi

if type notify-send >/dev/null 2>&1
then
    notify-send "rgit.sh" "$message"
fi

exit $returncode
