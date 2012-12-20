#!/bin/sh

git=`which git`

if test $? -ne 0
then
    echo "git not found." 1>&2
    exit 1
fi

name=`$git config user.name`

echo PATH = $git
echo NAME = $name
echo
$git show-branch -a
echo
$git diff --stat
