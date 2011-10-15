#!/bin/sh

LANG=C

type df >/dev/null 2>&1 && {
    df -h 2>/dev/null | grep --color=never --invert-match ^none
}

type xrandr >/dev/null 2>&1 && {
    xrandr | grep --color=never ^Screen
}
