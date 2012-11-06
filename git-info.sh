#!/bin/sh

git=`which git`

if test $? -ne 0
then
    exit $?
fi

name=`$git config user.name`

echo PATH = $git
echo NAME = $name
echo
$git show-branch -a
echo
$git status -s
