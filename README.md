save.sh
=======

Very simple backup utility using rsync.

Usage
-----

    save: save [-h] [d dst] file ...



***

chit.pl
=======

Take one line notes.



***

git-dumphead.sh
===============

Create archive of HEAD of current git repository.
Uses `txz` format if available, otherwise uses tgz.



***

git-wc.py
=========

See you have done great work (or done nothing).



***

git-diary.sh
============

Add diary to your git repository. Diaries are stored as commits in a orphan
branch.


Install
-------

Copy git-diary.sh and rename it to `git-diary`, then run

    $ git diary help


Available commands
------------------

### `add [<strings>]`

Add a new diary commit. When passing strings, you do not need to quote it using
`"` because they are automatically joined with whitespaces. If strings are
ommitted, git-diary launch the editor you configured for the git repository.

### `show [<options>]`

Show diaries. \<options\> are passed to `git log`.

### `help`

Show help message.


Configs
-------

All configs are stored under diary section. For example, if you want to change
branch name for diary, run:

    $ git config --add diary.branch notes

### `branch` (default: diary)

Branch name used for storing diary commits.

### `defcommand` (default: help)

Default command to run when no command is specified.

### `show.options` (default: "--oneline --reverse")

Options of `git log` used for `show` command.


TODOs
-----

* supress useless outputs
