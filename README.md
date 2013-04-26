save.sh
=======

Very simple backup utility using rsync.

Usage
-----

    save: save [-h] [-d <dst>] file ...

`save.sh` creates directory like `20130409-225834` in the destination directory
and copy files into that.

The destination directory is decided by `$SAVE_PATH` and it can be overwitten by
`-d` option. This value can be like `/path/of/dir/`, `user@host:` or
`user@host:/path/`. If neither `$SAVE_PATH` nor `-d <dst>` is privided,
or only `user@host:` is provided, `$HOME/.var/saved` is used for the directory.



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

### `list [<option> ...]`

Show diaries. Options are passed to `git diary-list` so you can use options for
`git log` like `--grep=todo`.

### `help`

Show help message.


Configs
-------

### `diary.branch` (default: diary)

Branch name used for storing diary commits.

### `diary.editor`

Editor used when running `git diary add` without texts. If `diary.editor` is not
set, default editor of git is used.

### `alias.diary-list`

Command used for `git diary list`. If not set yet, `"log"` is set automatically.



***

gitmemo.sh
==========

Take notes using git-diary.

Usage
-----

    usage: gitmemo init <path>
       or: gitmemo <command_for_git_diary> [arg ...]
       or: gitmemo git [<options_for_git> ...]
       or: gitmemo pull [arg ...]
       or: gitmemo push [arg ...]
       or: gitmemo config [arg ...]
       or: gitmemo help [<command>]

Configs
-------

Configs for git-diary are available, in addition to these configs.

### `memo.path`

Directory path used to store memo repository.
