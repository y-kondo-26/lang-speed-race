# 5言語の速さ比べ

C++・Rust・Go・JavaScript（Node.js）・Python が同じ問題を解いたときの実測時間を、アニメーションで再生して比べるページです。

- 10種類のベンチマーク（n-body、spectral-norm、mandelbrot、fannkuch-redux、binary-trees、fasta、k-nucleotide、reverse-complement、regex-redux、pidigits）を選べます。
- 「繰り返し」では、各言語が問題を解き終わるたびに最初から解き直し、解いた回数を数えます。「1回勝負」では、ゴールの順位を表示します。
- 指標（経過時間・CPU 時間）と、手書き最適化（SIMD・unsafe・C の関数の直接呼び出し）を除くかどうかを切り替えられます。
- 下のドットプロットは、10種類の結果を「最速の言語との時間の比」でまとめて表示します。

## データの出典

Isaac Gouy. (n. d.). [The Computer Language Benchmarks Game](https://benchmarksgame-team.pages.debian.net/benchmarksgame/).

- 言語ペア比較ページ（`fastest/python3-gpp.html`、`rust-gpp.html`、`go-gpp.html`、`python3-node.html`）から、2026年11月24日に取得しました。
- 測定環境は Intel Core i5-3330（4コア 3.0GHz）、Ubuntu 24.04、測定時期は2025年1〜2月です。
- 測定したバージョンは g++ 14.2.0、rustc 1.84.1、Go 1.23.1、Node.js 23.8.0、CPython 3.13.0 です。

ページはブラウザの中でベンチマークを実行しません。測定時間の比に合わせてアニメーションを再生します。

## ファイル

| パス | 内容 |
|---|---|
| `docs/index.html` | GitHub Pages が配信するページ（`build.sh` が生成する） |
| `src/*.part` | ページの部品。修正はここで行う |
| `data/benchmarks.json` | 取り出した実測値（230プログラム分） |
| `tools/extract.py` | 比較ページの HTML から実測値を取り出す |
| `tools/make_data.py` | `benchmarks.json` をページに埋め込む部品に変換する |

## 作り直し方

```sh
./build.sh   # src/*.part と data/benchmarks.json から docs/index.html を作る
./check.sh   # 埋め込んだ JavaScript の構文を確認する
```

データを取り直すときは、比較ページ4つを1つのディレクトリに `f_python3-gpp.html` などの名前で保存してから、次を実行します。

```sh
python3 -I tools/extract.py <保存したディレクトリ> > data/benchmarks.json
./build.sh
```
