"""PLAN-KUR-3 d4 (a): plan_kur.py sabit metinlerinde + 10 ölçüm işinin çıktısında kurulu-olmayan TAM katalog adı (kos.py sayacıyla aynı)."""
import contextlib, io, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / "tools"))
import plan_kur as pk  # noqa: E402
import katalog_ara as ka  # noqa: E402

kur = {o["ad"].lower() for o in pk.kayitlar() if ka.kurulu(o)}
yasak = {o["ad"].lower() for o in pk.kayitlar() if not ka.kurulu(o) and (len(o["ad"]) > 4 or "-" in o["ad"] or ":" in o["ad"])} - kur


def bul(m):
    return sorted(w for w in yasak if re.search(rf"(?<![\w:-]){re.escape(w)}(?![\w-])", m.lower()))


sabit = [pk.BASLIK, pk.KONSEY, *pk.SABIT.values(), *(k for _, _, k in pk.KAPI), *(x for v in pk.TUR.values() for x in v[1:])]
print("sabit:", bul("\n".join(sabit)))
IS = [s.split("\t")[2] for s in (WT / "tests" / "fixtures" / "plan_kur3_isler.tsv").read_text(encoding="utf8").splitlines()[1:]]
for n, q in enumerate(IS, 1):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        pk.plan_girdisi(q)
    print(n, bul(f.getvalue()))
