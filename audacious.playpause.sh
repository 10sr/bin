#!/bin/sh

# player=audacious
# if [ -n "$1" ]; then
#     player=$1
# fi

audver=$(audtool --version)

if [ -n "${audver}" ]; then
    audtool --playback-playpause
else
    # cd ~/Music
    # dir=$(zenity --file-selection --directory)
    # if [ -n "${dir}" ]; then
    #     audacious "${dir}" &
    # fi
    audacious &
fi

#echo ${dir}
