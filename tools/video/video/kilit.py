"""KİLİT-1: süreçler arası dosya kilidi — <dosya>.kilit O_EXCL ile alınır; zaman aşımı + bayat kilit temizliği."""
import os
import time
from contextlib import contextmanager
from pathlib import Path

BEKLE_SN, BAYAT_SN = 60, 120  # kilitli işler ms sürer; 120 sn'den eski kilit çökmüş süreçten kalmıştır


@contextmanager
def kilit(yol, bekle=BEKLE_SN, bayat=BAYAT_SN):
    k = Path(f"{yol}.kilit")
    k.parent.mkdir(parents=True, exist_ok=True)
    son = time.monotonic() + bekle
    while True:
        try:
            fd = os.open(k, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except (FileExistsError, PermissionError):  # Windows: silinmekte olan dosyada PermissionError
            try:
                if time.time() - k.stat().st_mtime > bayat:
                    k.unlink(missing_ok=True)  # ponytail: bayat kilit silme yarışı (iki süreç aynı anda) 120 sn eşiğinde ihmal edildi
                    continue
            except OSError:
                continue
            if time.monotonic() > son:
                raise TimeoutError(f"kilit: {k} {bekle} sn içinde alınamadı")
            time.sleep(0.01)
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        for _ in range(100):  # Windows: bekleyenin stat'ı anlık PermissionError verebilir
            try:
                k.unlink(missing_ok=True)
                break
            except PermissionError:
                time.sleep(0.01)
