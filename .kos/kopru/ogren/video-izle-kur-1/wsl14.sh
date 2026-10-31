#!/bin/bash
# TUR 13b: FreeToken — kok neden ft4.log:757 Python.h yok (venv py3.14) -> python3.14-dev
L=~/vik9/wsl13.log
echo "BASLA14 $(date +%H:%M) $(~/vik9/freetoken-venv/bin/python -V)" >> $L
export DEBIAN_FRONTEND=noninteractive
sudo -n apt-get install -y python3.14-dev >> ~/vik9/cuda13-apt.log 2>&1
echo "DEV rc=$? $(ls /usr/include/python3.14/Python.h 2>&1)" >> $L
export CUDA_HOME=/usr/local/cuda-13.0 PATH=/usr/local/cuda-13.0/bin:$PATH TMPDIR=~/vik9/tmp
timeout 3600 nice -n 10 ~/vik9/freetoken-venv/bin/pip install "freetoken[accel]" > ~/vik9/ft5.log 2>&1
echo "FT rc=$? $(date +%H:%M)" >> $L
~/vik9/freetoken-venv/bin/python -c "import freetoken,torch;print('FT_IMPORT_OK',torch.__version__,torch.version.cuda,torch.cuda.is_available())" >> $L 2>&1
ls ~/vik9/freetoken-venv/bin | grep -i free >> $L
echo "BITTI14 $(date +%H:%M)" >> $L
