#!/bin/bash
# TUR 12: tcl-lsp (Windows'ta std::os::unix -> WSL) + FreeToken (CUDA_HOME -> apt nvidia-cuda-toolkit)
L=~/vik9/wsl12.log
echo "BASLA $(date +%H:%M)" >> $L
# tcl-lsp
if [ ! -x ~/.cargo/bin/cargo ]; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal >> $L 2>&1
fi
source ~/.cargo/env
mkdir -p ~/vik9/tcl-lsp
rsync -a --delete --exclude target --exclude .git /mnt/c/Projeler/araclar/video-izle-kur-1/tcl-lsp/src/ ~/vik9/tcl-lsp/ >> $L 2>&1
cd ~/vik9/tcl-lsp
timeout 5400 nice -n 10 cargo build --release -p tcl-cli -j 3 > ~/vik9/tcl-build.log 2>&1
echo "TCL rc=$? $(date +%H:%M)" >> $L
ls target/release/ 2>/dev/null | grep -E '^tcl' >> $L
for b in target/release/tcl target/release/tcl-lsp; do [ -x $b ] && { echo "== $b --help" >> $L; $b --help 2>&1 | head -15 >> $L; }; done
# FreeToken
export DEBIAN_FRONTEND=noninteractive
which nvcc >/dev/null || sudo -n apt-get install -y nvidia-cuda-toolkit > ~/vik9/cuda-apt.log 2>&1
echo "NVCC $(nvcc --version 2>&1 | tail -1)" >> $L
export CUDA_HOME=/usr TMPDIR=~/vik9/tmp
mkdir -p $TMPDIR
timeout 3600 nice -n 10 ~/vik9/freetoken-venv/bin/pip install "freetoken[accel]" > ~/vik9/ft3.log 2>&1
echo "FT rc=$? $(date +%H:%M)" >> $L
~/vik9/freetoken-venv/bin/python -c "import freetoken,torch;print('FT_IMPORT_OK',getattr(freetoken,'__version__','?'),torch.__version__,torch.version.cuda,torch.cuda.is_available())" >> $L 2>&1
ls ~/vik9/freetoken-venv/bin | grep -i free >> $L
echo "BITTI $(date +%H:%M)" >> $L
