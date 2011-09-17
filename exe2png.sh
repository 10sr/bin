#!/bin/bash
# http://linuxos.blog102.fc2.com/blog-entry-125.html
# extract icon from windows exe file.
wrestool -x --output="$PWD" -t14 "$PWD/$1"
convert "$PWD/$1"_14_* "${1%.*}.png"
rm "$PWD/$1"_14_*
