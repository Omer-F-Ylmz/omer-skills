"""TOKEN-4 onay betiği — Desktop koşar (Ömer onayından sonra). VEKİL: settings.json/ANTHROPIC_BASE_URL'ye dokunmaz.
(a) A6: profiller/cc-arka.json "ajan" profiline yerleşik araç izin listesi (cc_profil "araclar" → --tools).
    Ölçüm (docs/kutuphane/olcum/token-4-a6*.tsv, count_tokens): köprü tur başı sabit bağlam 53 618 → 33 478 token (−%37.6).
    Dışarıda kalan 13 araç 7 günde 2803 oturumda: 11'i 0 kez, Workflow 4, ListAgents 1 (köprü işlerinde gerekmez).

  python onay/token_4_uygula.py --kuru   # plan (varsayılan)
  python onay/token_4_uygula.py uygula   # yedek → (a)
  python onay/token_4_uygula.py --geri   # yedeği geri koyar"""
import json
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
ARACLAR = ["Agent", "Bash", "Edit", "Glob", "Grep", "Monitor", "PowerShell", "Read", "ScheduleWakeup", "SendMessage",
           "TaskStop", "WebFetch", "WebSearch", "Write"]
ONCE = b'"ajan": {'
SATIR = b'"araclar": ' + json.dumps(ARACLAR).encode() + b', '


def plan(profil):
    b = profil.read_bytes()
    if "araclar" in json.loads(b)["ajan"]:
        print("(a) ajan profili: zaten araclar var")
    else:
        print("(a) ajan profili:", "eklenecek →" if b.count(ONCE) == 1 else "BİÇİM BEKLENMEDİK — elle bak", ",".join(ARACLAR))
    return 0


def uygula(profil):
    b = profil.read_bytes()
    if "araclar" in json.loads(b)["ajan"] or b.count(ONCE) != 1:
        return plan(profil) or 1
    shutil.copy2(profil, profil.with_suffix(".json.token4-yedek"))
    yeni = b.replace(ONCE, ONCE + SATIR)  # bayt düzeyi: CRLF ve girinti korunur
    json.loads(yeni)
    profil.write_bytes(yeni)
    print("uygulandı · yedek", profil.with_suffix(".json.token4-yedek"))
    return 0


def geri(profil):
    y = profil.with_suffix(".json.token4-yedek")
    if not y.exists():
        print("yedek yok")
        return 1
    shutil.move(y, profil)
    print("geri alındı:", profil)
    return 0


def main(argv=None, profil=KOK / "profiller" / "cc-arka.json"):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    return {"--kuru": plan, "uygula": uygula, "--geri": geri}[a[0]](profil)


if __name__ == "__main__":
    sys.exit(main())
