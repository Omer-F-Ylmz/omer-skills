"""TOKEN-2 d4 K1b-klon: A kolu = 6769 test vekili, 6768'in HEADROOM_* ortamının kopyası + --log-messages; doğal tetik istem-r0e-B, 1 claude -p.
Değer yazdırılmaz; yalnız ad listesi k1c_adlar.txt'ye. Paylaşılan durum dosyaları (öğrenilmiş TTL, yakalama) geçici kopyaya yönlendirilir.
Kullanım: python k1c.py [ad1,ad2,...]  — ad listesi verilirse yalnız o alt küme kopyalanır (ikiye bölme için)."""
import json, os, shutil, sys, time
from pathlib import Path

import psutil

D = Path(__file__).parent
sys.path.insert(0, str(D)); sys.path.insert(0, r"C:\Users\pc\Desktop\TELVE-wt\token1\docs\r1\_ham\token1")
import ab_r0e  # noqa: E402
from k1_dogrula import kol  # noqa: E402

IZIN = ("--permission-mode", "acceptEdits", "--allowedTools", "Read,Edit,Write,Glob,Grep,Bash")  # k1b ile aynı; k1b import edilmez (__main__ koruması yok)


def kaynak_env():
    for c in psutil.net_connections("tcp"):
        if c.laddr and c.laddr.port == 6768 and c.status == "LISTEN":
            # d4 VEKİL KAZASI: CC_SWITCH_* kopyalanınca 6769 uzlaştırıcıyı kendi çalıştırıp ~/.claude/settings.json'u kendine çevirdi
            return {k: v for k, v in psutil.Process(c.pid).environ().items()
                    if k.startswith("HEADROOM_") and k != "HEADROOM_PORT" and not k.startswith("HEADROOM_CC_SWITCH_")}
    sys.exit("6768 dinlemiyor")


KORU = [Path.home() / ".claude/settings.json", Path(os.environ["LOCALAPPDATA"]) / "Headroom/config/cc-switch-upstream.json"]
ONCE = {p: p.read_bytes() for p in KORU if p.is_file()}


env = kaynak_env()
if len(sys.argv) > 1:
    env = {k: v for k, v in env.items() if k in sys.argv[1].split(",")}
gec = D / "k1c_gecici"; gec.mkdir(exist_ok=True)
for k in ("HEADROOM_CACHE_TTL_LEARNED_PATH", "HEADROOM_CC_SWITCH_CAPTURE_PATH"):
    if k in env:  # 6768'in canlı dosyasını kirletmesin
        h = gec / Path(env[k]).name
        if Path(env[k]).is_file():
            shutil.copy2(env[k], h)
        env[k] = str(h)
(D / "k1c_adlar.txt").write_text("\n".join(sorted(env)) + "\n" + json.dumps(
    {"proxy_url_6768_iceriyor": "6768" in env.get("HEADROOM_CC_SWITCH_PROXY_URL", "")}) + "\n", encoding="utf-8")
while psutil.virtual_memory().percent >= 85:
    print("RAM", psutil.virtual_memory().percent, "bekle", flush=True); time.sleep(60)
w = ab_r0e.kur("B")
try:
    r = kol("c_A_klon", env, istem=ab_r0e.istem("B"), cwd=w, tur=12, ek=IZIN, sure=1500, vekil_ek=("--log-messages",))
finally:
    ab_r0e.sil("B")
    for p, b in ONCE.items():  # global ayar değiştiyse geri yaz, kaydet
        if p.read_bytes() != b:
            p.write_bytes(b); print("UYARI geri yazıldı:", p.name, flush=True)
if "onbelleksiz" in r:
    r["agirlikli_giris"] = round(r["onbelleksiz"] + 0.1 * r["okuma"] + 1.25 * r["yazma"])
r["kopya_ad"] = len(env)
print(json.dumps(r, ensure_ascii=False), flush=True)
with open(D / "k1b.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("BITTI", flush=True)
