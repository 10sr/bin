#!/bin/sh
git=`which git`

if test $? -ne 0
then
    echo "git not found." 1>&2
    exit 1
fi



name=`$git config user.name`
email=`$git config user.email`

echo PATH = $git
echo NAME = $name
echo MAIL = $email
echo
$git show-branch --all && \
    echo && \
    $git diff --stat
