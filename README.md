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

Write diaries in your git repository. Diaries are stored as messages of commits
in a orphan branch.


Install
-------

Copy git-diary.sh and rename it to `git-diary`, then run

    $ git diary


Available commands
------------------

### `add [<text> ...]`

Add a new diary commit. When passing texts, you do not need to quote them
using `"` because they are automatically joined with whitespaces.

When texts are not specified, git-diary launches editor.

### `show [<option> ...]`

Show diaries. Options are passed to `git diary-show` so you can use options for
`git log` like `--grep=todo`.

### `help`

Show help message.


Configs
-------

### `diary.branch` (default: diary)

Branch name used for storing diary commits.

### `diary.defcommand` (default: help)

Default command to run when no command is specified.

### `diary.editor`

Editor used when running `git diary add` without texts. If `diary.editor` is not
set, default editor of git is used.

### `alias.diary-show`

Command used for `git diary show`. If not set yet, following alias is set
automatically.

    "log --reverse --pretty=tformat:\"%C(yellow)%ai%C(reset) [%C(red)%an%C(reset)] %C(white bold)%s%C(reset)\""

