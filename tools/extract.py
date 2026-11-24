"""Benchmarks Game の言語ペア比較ページ (fastest/*.html) から実測値を取り出し、JSON にする。

使い方: python3 -I tools/extract.py <ページを保存したディレクトリ> > data/benchmarks.json
入力: f_python3-gpp.html, f_rust-gpp.html, f_go-gpp.html, f_python3-node.html
"""
import html
import json
import re
import sys
from pathlib import Path

LANG = {"gpp": "cpp", "rust": "rust", "go": "go", "node": "node", "python3": "python"}
PAGES = ["f_python3-gpp.html", "f_rust-gpp.html", "f_go-gpp.html", "f_python3-node.html"]


def num(s):
    s = s.replace(",", "").strip()
    return float(s)


def parse(path):
    t = path.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'<tbody id="([^"]+)">(.*?)(?=<tbody id=|</table>)', t, re.S):
        bench, body = m.group(1), m.group(2)
        for row in re.split(r"<tr>", body):
            tds = re.split(r"<td>", row)[1:]
            if len(tds) < 6:
                continue
            href = re.search(r'program/([a-z0-9]+)-([a-z0-9]+)-?(\d*)\.html', tds[0])
            if not href:
                continue
            code, ver = href.group(2), href.group(3) or "1"
            if code not in LANG:
                continue
            label = html.unescape(re.sub(r"<[^>]+>", "", tds[0])).replace("\xa0", " ").strip()
            flagged = label.startswith("*") or "*" in tds[0].split("<a")[0]
            cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in tds[1:6]]
            try:
                secs = num(cells[0])
            except ValueError:
                continue  # Bad Output / Timed Out など
            cpu = cells[1].split("—")
            cpu = sum(num(c) for c in cpu) / len(cpu)
            out.append({
                "bench": bench, "lang": LANG[code], "prog": f"{href.group(1)}-{code}-{ver}",
                "label": label.lstrip("* ").strip(), "flagged": flagged,
                "secs": secs, "cpu": round(cpu, 2), "memKiB": int(num(cells[2])), "gz": int(num(cells[3])),
            })
    return out


def main():
    d = Path(sys.argv[1])
    seen = {}
    for p in PAGES:
        for r in parse(d / p):
            seen[r["prog"]] = r  # 同じプログラムが複数ページに出るので重複を除く
    rows = sorted(seen.values(), key=lambda r: (r["bench"], r["lang"], r["secs"]))
    json.dump(rows, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
