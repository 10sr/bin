#!/usr/bin/env python3
# %%%{CotEditorXInput=AllText}%%%
# %%%{CotEditorXOutput=ReplaceAllText}%%%

import sys
for l in sys.stdin:
    lu = l
    trans = lu.maketrans("。、", "．，")
    print(lu.translate(trans), end="")