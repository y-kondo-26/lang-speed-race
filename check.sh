#!/bin/sh
# docs/index.html の <script> を取り出して構文を確認する
set -e
T="$(mktemp -d)/check.js"
cd "$(dirname "$0")"
python3 -I -c "
import re,sys
t=open('docs/index.html',encoding='utf-8').read()
s=re.findall(r'<script>(.*?)</script>',t,re.S)
open(sys.argv[1],'w').write('\n'.join(s))" "$T"
node --check "$T" && echo "JS syntax OK"
