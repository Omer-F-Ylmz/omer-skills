"""TOKEN-2 d5 K1c: gerçek iş yükü (geçici klasörde 11 büyük metin + 1 görüntü, adım başı ≥5k yeni token), tek kol, 1 claude -p.
A = 6768 HEADROOM_* klonu (k1c ile aynı) · B = klon + HEADROOM_STABLE_BOUNDARY_BREAKPOINT=0. opus, effort low, max-turns 14.
Kullanım: python k1d.py A|B [en_az_bayt=24000]  — durma %, ağırlıklı (g + 1.25·cw + 0.1·cr + 5·ç), sıkıştırma, tam yeniden yazım + adım arası sn."""
import glob, json, os, shutil, sys, tempfile, time
from datetime import datetime
from pathlib import Path

import psutil

D = Path(__file__).parent; KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(D))
from k1_dogrula import kol  # noqa: E402

KORU = [Path.home() / ".claude/settings.json", Path(os.environ["LOCALAPPDATA"]) / "Headroom/config/cc-switch-upstream.json"]
ONCE = {p: p.read_bytes() for p in KORU if p.is_file()}


def kaynak_env():  # k1c.py'den (o betik import edilemez: __main__ koruması yok)
    for c in psutil.net_connections("tcp"):
        if c.laddr and c.laddr.port == 6768 and c.status == "LISTEN":
            return {k: v for k, v in psutil.Process(c.pid).environ().items()
                    if k.startswith("HEADROOM_") and k != "HEADROOM_PORT" and not k.startswith("HEADROOM_CC_SWITCH_")}
    sys.exit("6768 dinlemiyor")


def adimlar(sid):
    tr = next((Path.home() / ".claude/projects").glob(f"*/{sid}.jsonl"))
    goruldu, a = set(), []
    for l in open(tr, encoding="utf-8"):
        r = json.loads(l); m = r.get("message") or {}
        u = m.get("usage")
        if r.get("type") != "assistant" or not u or m.get("id") in goruldu:
            continue
        goruldu.add(m.get("id"))
        a.append((u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0),
                  u.get("output_tokens", 0), datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")).timestamp()))
    return a


ad = sys.argv[1]; en_az = int(sys.argv[2]) if len(sys.argv) > 2 else 24000
env = kaynak_env()
if ad == "B":
    env["HEADROOM_STABLE_BOUNDARY_BREAKPOINT"] = "0"
gec = D / "k1c_gecici"; gec.mkdir(exist_ok=True)
for k in ("HEADROOM_CACHE_TTL_LEARNED_PATH", "HEADROOM_CC_SWITCH_CAPTURE_PATH"):
    if k in env:  # 6768'in canlı dosyasını kirletmesin
        h = gec / Path(env[k]).name
        if Path(env[k]).is_file():
            shutil.copy2(env[k], h)
        env[k] = str(h)
w = Path(tempfile.mkdtemp(prefix="k1d_"))
metin = sorted(f for f in glob.glob(str(KOK / "docs/video-tarama/*.md")) if en_az < os.path.getsize(f) < en_az * 1.4)[:11]
adlar = []
for i, f in enumerate(metin, 1):
    shutil.copy2(f, w / f"f{i:02d}.md"); adlar.append(f"f{i:02d}.md")
shutil.copy2(KOK / "dist/telve-r1/r1-b.png", w / "g07.png"); adlar.insert(6, "g07.png")
istem = ("Use the Read tool on each of these files in this folder, ONE file per call, strictly sequentially (never parallel; no Bash, Grep or Glob). "
         "After each file, think briefly about its main topic. After the last one, reply with exactly one line: the number of files you read.\n" + "\n".join(adlar))
while psutil.virtual_memory().percent >= 85:
    print("RAM", psutil.virtual_memory().percent, "bekle", flush=True); time.sleep(60)
try:
    r = kol(f"d_{ad}", env, istem=istem, cwd=w, tur=14, ek=("--allowedTools", "Read"), sure=1500, vekil_ek=("--log-messages",), effort="low")
finally:
    shutil.rmtree(w, ignore_errors=True)
    for p, b in ONCE.items():  # global ayar değiştiyse geri yaz
        if p.read_bytes() != b:
            p.write_bytes(b); print("UYARI geri yazıldı:", p.name, flush=True)
if "sid" in r:
    a = adimlar(r["sid"])
    g, cw, cr, c = (sum(x[k] for x in a) for k in range(4))
    r["durma_yuzde"] = round(100 * r["durma"] / max(len(a), 1))
    r["agirlikli"] = round(g + 1.25 * cw + 0.1 * cr + 5 * c)
    r["cikti_top"] = c
    r["yeniden_yazim"] = [{"adim": i + 1, "cr_once": a[i - 1][2], "cr": x[2], "cw": x[1], "ara_sn": round(x[4] - a[i - 1][4])}
                          for i, x in enumerate(a) if i and x[2] < 0.5 * a[i - 1][2] and x[1] > 20000]
    r["adimlar"] = [x[:4] for x in a]
r["dosya_bayt"] = en_az; r["kopya_ad"] = len(env)
print(json.dumps(r, ensure_ascii=False), flush=True)
with open(D / "k1d.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("BITTI", flush=True)
