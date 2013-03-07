#!/bin/sh

# usage: $0 u[p]|d[own]|l[eft]|r[ight]
# works poorly when $all % $rows != 0

rows=2

if ! type wmctrl >/dev/null 2>&1
then
    echo "$0 requires wmctrl. Install it first."
    exit 1
fi

help(){
    cat <<__EOC__
usage: $0 u|d|l|r
__EOC__
}

all=`wmctrl -d | wc -l`

cols=`expr $all / $rows`
current=`wmctrl -d | grep '*' | cut -f 1 -d ' '`

# vals: all, rows, cols, current

get_up(){
    new=`expr $current - $cols`
    if test $new -lt 0
    then
        echo $current
    else
        echo $new
    fi
}

get_down(){
    new=`expr $current + $cols`
    if test $new -ge $all
    then
        echo $current
    else
        echo $new
    fi
}

get_left(){
    new=`expr $current - 1`
    if test $new -lt 0
    then
        echo `expr $all - 1`
    else
        echo $new
    fi
}

get_right(){
    new=`expr $current + 1`
    if test $new -ge $all
    then
        echo 0
    else
        echo $new
    fi
}

go(){
    wmctrl -s `get_$1`
}

case $1 in
    u*) go up;;
    d*) go down;;
    l*) go left;;
    r*) go right;;
    *) help;;
esac
