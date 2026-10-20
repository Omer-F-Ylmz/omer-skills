"""TOKEN-REA rtk2 onay betiği — Desktop koşar (Ömer onayından sonra). tools/rtk_onisle.py'ye rota ekler: ayraçsız tek `ls` / `git diff` (stat'sız) / `git status`
komutu `python -I -S .kos/kopru/token-rea/rtk2.py <komut>`'a yazılır (rtk2.tur() sınıflandırır; büyük çıktı özet + `rtk2.py ac <id>` ile tam metin).
Ölçüm (3 yeni tohum, uçtan uca): token rtk 92k → rtk2 3.4k, süre 1.63 → 1.18 sn, sinyal ≥ rtk. `find` rtk'da kalır (süre kaybı). Eski dosya <dosya>.token-rea-yedek.

  python onay/token_rea_rtk2.py --kuru   # plan (varsayılan)
  python onay/token_rea_rtk2.py uygula   # yedekle + yama
  python onay/token_rea_rtk2.py --geri   # yedekten geri yükle"""
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
ISARET = "# TOKEN-REA rtk2"
FONK = f'''

{ISARET}: süzgeçli tek komut rtk2'ye yazılır (rtk2.tur); tırnak/ayraç/yönlendirme olan komuta dokunmaz.
def rtk2_yaz(komut):
    if AYRAC.search(komut) or any(c in komut for c in "\\"'`$<>"):
        return None
    import importlib.util, os
    yol = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".kos", "kopru", "token-rea", "rtk2.py")
    if not os.path.exists(yol):
        return None
    ozel = importlib.util.spec_from_file_location("rtk2", yol)
    m = importlib.util.module_from_spec(ozel)
    ozel.loader.exec_module(m)
    argv = komut.split()
    return f"python -I -S {{yol}} {{komut.strip()}}" if argv and m.tur(argv) in ("ls", "diff", "durum") else None
'''
ESKI = '''    yeni = yeniden_yaz(komut, arac)
    if yeni is None or rtk_kontrol(ham):
        return 0
'''
YENI = f'''    r2 = rtk2_yaz(komut) if arac == "Bash" else None  {ISARET}
    yeni = r2 or yeniden_yaz(komut, arac)
    if yeni is None or (r2 is None and rtk_kontrol(ham)):
        return 0
'''


def yama(kaynak):
    assert ESKI in kaynak, "rtk_onisle.main beklenen biçimde değil"
    a = kaynak.index("\n\ndef main(")
    return kaynak[:a] + FONK + kaynak[a:].replace(ESKI, YENI)


def main(argv=None, dosya=KOK / "tools" / "rtk_onisle.py"):
    mod = (argv if argv is not None else sys.argv[1:] or ["--kuru"])[0]
    yedek = dosya.with_name(dosya.name + ".token-rea-yedek")
    ham = dosya.read_bytes().decode("utf-8")
    var = ISARET in ham
    if mod == "--kuru":
        print(f"{dosya}: {'zaten yamalı' if var else 'yama uygulanacak'}")
    elif mod == "uygula" and not var:
        if not yedek.exists(): yedek.write_bytes(dosya.read_bytes())
        crlf = "\r\n" in ham
        yeni = yama(ham.replace("\r\n", "\n"))
        dosya.write_bytes((yeni.replace("\n", "\r\n") if crlf else yeni).encode("utf-8"))  # bayt: write_text CRLF'ye çevirir
    elif mod == "--geri" and yedek.exists():
        shutil.copyfile(yedek, dosya)
    return 0


if __name__ == "__main__":
    sys.exit(main())
