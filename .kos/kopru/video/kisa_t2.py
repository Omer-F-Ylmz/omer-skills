"""VİDEO-KISA-TOKEN-2 ölçüm: aynı Gemini önbelleğiyle 14 video (altın 8 + sınama 6) tek calistir → karar (M1–M4), iki soğuk tekrar (karar.tsv yedeğe).
claude -p: koşu başı ⌈sorulan/120⌉ (beklenen 1) × 2. Eski tam-Claude raporları kisa/eski-tamclaude/'a bir kez yedeklenir (calistir aynı adla yazar)."""
import json
import shutil
import subprocess
import sys

import kisa_m4 as m4
from video import kisa

KT = m4.CIK / "karar.tsv"
ESKI = m4.CIK / "eski-tamclaude"
if not ESKI.is_dir():
    ESKI.mkdir()
    for f in m4.CIK.glob("ig-*.md"):
        shutil.copy(f, ESKI / f.name)
ids = m4.ALTIN + m4.EK + m4.SINAMA
for et in sys.argv[1:] or ("t2a", "t2b"):
    if KT.is_file():
        KT.replace(m4.CIK / f"karar-once-{et}.tsv")  # her tekrar soğuk: M2 önbelleği tekrarlar arası taşınmaz
    iz, y = kisa.calistir(ids, m4.ONB, m4.CIK, claude=True, sil=False)
    ad = f"oturum-{et}.json"
    (m4.CIK / ad).write_text(json.dumps({"iz": iz, "sonuc": y}, ensure_ascii=False, indent=1), encoding="utf-8")
    (m4.CIK / et).mkdir(exist_ok=True)
    for v in ids:
        shutil.copy(m4.CIK / f"{v}.md", m4.CIK / et / f"{v}.md")
    u, n = y["usage"], len(iz)
    print("##", et, "çağrı", y["cagri"], "sorulan", y["sorulan"], "kararlı", y["kararli"], "hata", y["hata"], "claude sn", y["sure"], "usd", y["usd"],
          "| girdi", u.get("input_tokens", 0), "cr", u.get("cache_read_input_tokens", 0), "cw", u.get("cache_creation_input_tokens", 0), "çıktı", u.get("output_tokens", 0),
          "| ağır/video", round(m4.agir(u.get("input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("output_tokens", 0)) / n),
          "| hazır sn/video", round(y["hazir_sure"] / n, 1), "duvar sn/video", round(y["duvar"] / n, 1), flush=True)
    for argv in (["puan", ad, "temiz"], ["sinama_puan", ad]):
        print("##", et, *argv, flush=True)
        subprocess.run([sys.executable, m4.__file__, *argv], check=False, stderr=subprocess.STDOUT)
for f in m4.CIK.glob("ig-*.md"):  # kisa/ kökü eski tam-Claude raporları olarak kalır (karar uyumu girdisi)
    shutil.copy(ESKI / f.name, f)
print("BITTI", flush=True)
