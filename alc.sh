#!/bin/bash
set -e
# Original: http://taka.no32.tk/diary/20050826.html

if ! which nkf >/dev/null
then
    echo nkf command not found
    echo Abort.
    exit 1
fi

if test -z "$1"
then
    cat <<__EOC__
usage: alc.sh <word-or-phrases> ...
__EOC__
fi

KEY=`echo $@ | nkf -w -w80`
echo $@ >> ~/.eng-list # 履歴を保存（不要なら削除）．
URI="http://eow.alc.co.jp/$KEY/UTF-8/"
RS=`echo '▼ 検索結果本体 ▼' | nkf -w -w80`
RE=`echo '▲ 検索結果本体 ▲' | nkf -w -w80`
wget -q --referer='http://eow.alc.co.jp/' -U 'Mozilla/5.0' -O - "$URI" | \
    sed -ne "/<!--\s*$RS\s*-->/,/<!--\s*$RE\s*-->/p" | \
    w3m -dump -T 'text/html'
