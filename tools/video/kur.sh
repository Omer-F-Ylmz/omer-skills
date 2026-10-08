#!/usr/bin/env bash
# 1b-1S S5: video aracını kurar. pyproject'teki override-dependencies `uv tool install`'da uygulanmaz; onnxruntime-directml'i
# fastembed'in onnxruntime'ı ezmesin diye override dosyayla verilir (yoksa DML düşer, künye "cpu (dml yok)").
set -euo pipefail
cd "$(dirname "$0")"
uv tool install --editable . --reinstall --overrides overrides.txt
