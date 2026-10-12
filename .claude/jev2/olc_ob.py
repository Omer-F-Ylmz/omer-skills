"""JEV-2 (a) ölçüm: ortak yargıç önbelleği — JEV-1 opus ref (n=50) üzerinde soğuk/sıcak koşu; uyum (Spearman/MAE) + $ + süre.
Tavan: Jev ≤ 60 HTTP istek (durum başına 1), claude -p 0 (opus ref JEV-1'den yeniden kullanılır)."""
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
WT = Path(__file__).resolve().parents[2]
J1 = Path("C:/Projeler/omer-skills-wt/jev/.claude/jev1")
sys.path[:0] = [str(WT / "tools" / "olcum"), str(WT / "tools" / "jev"), str(J1)]
import jev_yargic  # noqa: E402
from jev.cekirdek import Tasiyici  # noqa: E402
from karsilastir_ab import spearman  # noqa: E402  (JEV-1 ile aynı hesap)

jev1 = {k["dosya"]: k for k in map(json.loads, open(J1 / "jev_tum.jsonl", encoding="utf-8"))}
dos, opus = json.load(open(J1 / "ornek_sira.json")), json.load(open(J1 / "opus_ref.json"))
o = [opus[str(i)] * 2 for i in range(len(dos))]
mae = lambda a: round(sum(abs(x - y) for x, y in zip(a, o)) / len(o), 2)  # noqa: E731
ob = Path(__file__).parent / "olc_ob.json"
ob.unlink(missing_ok=True)
t = Tasiyici(en_fazla=2, istek_tavan=60)
for kol in ("soguk", "sicak"):
    k0, t0 = len(t.kullanim), time.perf_counter()
    c = jev_yargic.yargila([jev1[d]["state"] for d in dos], jev_yargic.SORU, t, ob)
    sure, u = time.perf_counter() - t0, t.kullanim[k0:]
    jv = [round(x["kalite"]["score"] * 2, 1) for x in c]
    print(f"{kol}: n={len(jv)} istek {len(u)} ${sum(float(x.get('cost') or 0) for x in u):.5f} süre {sure:.1f}s · "
          f"spearman jev~opus {spearman(jv, o)} MAE {mae(jv)}")
taban = [jev1[d]["jev"] for d in dos]
print(f"taban (JEV-1 tek koşu): spearman {spearman(taban, o)} MAE {mae(taban)}")
