#!/bin/sh

# add crontab as below to run this every 10 min
# */10 * * * * sh batterystate.sh

file=$HOME/.batterystatus

batterystatus(){
    local dir=/sys/class/power_supply/BAT0
    if test -d $dir
    then
        local st=$(cat $dir/status)
        local full=$(cat $dir/charge_full)
        local now=$(cat $dir/charge_now)
        local rate=$(expr $now \* 100 / $full)
        printf $1 "${st}:${rate}%"
    fi
}

batterystatus %s >$file
