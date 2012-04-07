#!/bin/sh
# copy some important files into current directory.

files="
/etc/rc.conf
/var/log/pacman.log
/etc/pacman.d/gnupg/gpg.conf
"

convpass(){
    echo $1 | sed -e 's / ! g'
}

for i in $files
do
    cp -fvu $i ./$(basename $i)
done

map=/usr/share/kbd/keymaps/i386/qwerty/myjp106.map
zcat ${map}.gz >./$(basename ${map}) &&
echo "\`$map\' -> \`./$(basename $map)\'"

pacman -Qqe | grep -vx "$(pacman -Qqm)" > ./pkg.lst &&
echo "Make pkg.lst."
