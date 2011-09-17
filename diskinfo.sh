#!/bin/sh

LANG=C

type df >/dev/null 2>&1 && {
    df -h | grep --color=never --invert-match ^none
}
