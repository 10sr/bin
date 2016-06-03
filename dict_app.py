#!/usr/bin/python2.7

# http://sakito.jp/mac/dictionary.html

import sys
import DictionaryServices as ds

def main():
    word = sys.argv[1].decode('utf-8')
    # for e in dir(ds):
    #     if e.startswith("DCS"):
    #         print(e)
    # return
    result = ds.DCSCopyTextDefinition(None, word, (0, len(word)))
    print result.encode('utf-8')

if __name__ == '__main__':
    main()
