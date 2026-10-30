#!/bin/bash
# VIDEO-IZLE-KUR-1 tur9: Cloudroom core (kaynaktan, install.sh yok) + FreeToken (install.sh yok, ayri venv) WSL Ubuntu'da.
# sonuc: /mnt/c/.../kur-tur9.tsv'ye satir; gunluk: wsl9.log
T=/mnt/c/Projeler/omer-skills/.kos/kopru/ogren/video-izle-kur-1/kur-tur9.tsv
yaz() { printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" >> "$T"; echo "$1 $2 $3"; }
son() { tr -s '\n\t' '  ' | tail -c 200; }
export DEBIAN_FRONTEND=noninteractive
sudo -n apt-get install -y -q cargo rustc python3-venv build-essential pkg-config libssl-dev >/tmp/apt9.log 2>&1 || echo "apt hata: $(tail -3 /tmp/apt9.log)"

# Cloudroom core
mkdir -p ~/vik9 && rm -rf ~/vik9/cloudroom && cp -r /mnt/c/Projeler/araclar/video-izle-kur-1/Cloudroom/src ~/vik9/cloudroom
cd ~/vik9/cloudroom/core
o=$(timeout 3000 cargo build --locked --release -j 2 2>&1); rc=$?
if [ $rc -ne 0 ]; then yaz Cloudroom basarisiz "WSL cargo build rc=$rc: $(echo "$o" | son)" "~/vik9/cloudroom/core"
else
  e=$(find target/release -maxdepth 1 -type f -executable | head -3 | tr '\n' ' ')
  h=$(for x in $e; do timeout 20 $x --help 2>&1 | head -5; done | son)
  yaz Cloudroom calisiyor "WSL cargo build --locked ok; exe: $e; --help: $h" "WSL ~/vik9/cloudroom/core"
fi

# FreeToken
python3 -m venv ~/vik9/freetoken-venv && . ~/vik9/freetoken-venv/bin/activate
o=$(timeout 2400 pip install -q "freetoken[accel]" 2>&1); rc=$?
if [ $rc -ne 0 ]; then yaz FreeToken basarisiz "WSL pip freetoken[accel] rc=$rc: $(echo "$o" | son)" "WSL ~/vik9/freetoken-venv"
else
  h=$( (timeout 60 freetoken --help 2>&1 || timeout 60 python -c "import freetoken;print('import ok',freetoken.__file__)" 2>&1) | son)
  yaz FreeToken calisiyor "WSL ayri venv pip freetoken[accel] ok; $h" "WSL ~/vik9/freetoken-venv"
fi
echo BITTI
