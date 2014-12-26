synk.sh
=======

Simple file synchronization utility.

Syncronize files in current directory to the pre-defined remote directory
with the simple commands `synk {pull|push}`.


Usage
-----

    synk [-h] {push|pull|info}

First you need to create a file named `.synk.conf`, which is a shellscript.
This file may contain some variable definitions:

* remote=[[user]@host:]dir (required):
    Remote directory to synk files with.
* rsync_opts:
    Additional arguments for rsync command.

The directory containing `.synk.conf` is considered to be the "root" of
the directory to synk. Even if you issue `synk` in "subdirectories", synk is
done from the "root" directory.



License
-------

This software is unlicensed.
