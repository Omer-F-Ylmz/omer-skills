"""Atomik yazım: tmp → os.replace. Windows'ta hedef dosya başka süreçte açıkken (okuyucu) os.replace WinError 5 verir;
kısa geri çekilmeyle yeniden denenir. Son deneme de düşerse istisna yükselir; çağıran döngü logla, sonraki turda dener."""
import os
import random
import time
from pathlib import Path

DENEME = 5


def yaz_bayt(yol, veri):
    yol = Path(yol)
    yol.parent.mkdir(parents=True, exist_ok=True)
    t = yol.with_suffix(f".{os.getpid()}.tmp")  # süreç başı tmp: ortak .tmp Windows'ta çakışıyordu
    t.write_bytes(veri)
    for i in range(DENEME):
        try:
            return os.replace(t, yol)
        except PermissionError:
            if i == DENEME - 1:
                t.unlink(missing_ok=True)
                raise
            time.sleep(random.uniform(0.05, 0.4))
