#!/bin/bash

export DISPLAY=:0.0
export LANG=ja_JP.UTF-8

.exec 10> >(zenity --notification --listen --window-icon "/usr/share/pixmaps/none.png")
echo "visible: false" >&10

echo "message: $1" >&10
sleep 1
exec 10>&-
