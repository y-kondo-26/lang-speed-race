"""data/benchmarks.json を、ページに埋め込む <script> 部品 (src/20-data.part) に変換する。

使い方: python3 -I tools/make_data.py data/benchmarks.json > src/20-data.part
"""
import json
import sys

rows = json.load(open(sys.argv[1], encoding="utf-8"))
keep = ["bench", "lang", "prog", "label", "flagged", "secs", "cpu", "memKiB"]
slim = [{k: r[k] for k in keep} for r in rows]
print("<script>")
print("// 出典: The Computer Language Benchmarks Game（fastest/*.html、2026-11-24 取得）。tools/extract.py で生成")
print("const ROWS = " + json.dumps(slim, ensure_ascii=False, separators=(",", ":")) + ";")
