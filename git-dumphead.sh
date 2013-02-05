#!/bin/sh
startdir="$PWD"

toppath="`git rev-parse --show-toplevel 2>/dev/null`" || exit $?

cd "$toppath"

current="`git rev-parse --short HEAD`"

get_rep_name(){
    rurl="`git config --get remote.origin.url`"
    if test -n "$rurl"
    then
        name="`basename "$rurl" .git`"
    else
        name="`basename "$toppath" .git`"
    fi
    echo "$name"
}

repname="`get_rep_name`"
outname="$repname-$current"

decide_format(){
    if git config --get tar.txz.command >/dev/null
    then
        fmt=txz
    else
        fmt=tgz
    fi
    echo $fmt
}

fmt=`decide_format`

echo "Start creating archive dump of HEAD."
git archive --verbose --prefix="$outname/" \
    --output="$startdir/$outname.$fmt" HEAD
echo "Dump created as '$outname.$fmt'."
