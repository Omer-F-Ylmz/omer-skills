#!/bin/bash
# TUR 13: FreeToken — torch 2.11 cu130 ister, apt nvcc 12.4 uyumsuz -> NVIDIA wsl-ubuntu deposundan cuda-toolkit-13-0
L=~/vik9/wsl13.log
echo "BASLA $(date +%H:%M)" >> $L
export DEBIAN_FRONTEND=noninteractive
cd ~/vik9
[ -f cuda-keyring_1.1-1_all.deb ] || wget -q https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo -n dpkg -i cuda-keyring_1.1-1_all.deb >> $L 2>&1
sudo -n apt-get update > ~/vik9/cuda13-apt.log 2>&1
sudo -n apt-get install -y cuda-toolkit-13-0 >> ~/vik9/cuda13-apt.log 2>&1
echo "APT rc=$? $(/usr/local/cuda-13.0/bin/nvcc --version 2>&1 | tail -1)" >> $L
export CUDA_HOME=/usr/local/cuda-13.0 PATH=/usr/local/cuda-13.0/bin:$PATH TMPDIR=~/vik9/tmp
timeout 3600 nice -n 10 ~/vik9/freetoken-venv/bin/pip install "freetoken[accel]" > ~/vik9/ft4.log 2>&1
echo "FT rc=$? $(date +%H:%M)" >> $L
~/vik9/freetoken-venv/bin/python -c "import freetoken,torch;print('FT_IMPORT_OK',getattr(freetoken,'__version__','?'),torch.__version__,torch.version.cuda,torch.cuda.is_available())" >> $L 2>&1
ls ~/vik9/freetoken-venv/bin | grep -i free >> $L
echo "BITTI $(date +%H:%M)" >> $L
