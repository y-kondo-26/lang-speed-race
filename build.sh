#!/bin/sh
# 部品 (src/*.part) と実測データ (data/benchmarks.json) から docs/index.html を作る
set -e
cd "$(dirname "$0")"
python3 -I tools/make_data.py data/benchmarks.json > src/20-data.part
cat src/00-head.part src/10-body.part src/20-data.part src/30-viz.part src/40-sim.part src/50-chart.part src/90-tail.part > docs/index.html
echo "docs/index.html: $(wc -c < docs/index.html) bytes"
