"""RUFLO-1 onay betiği — Desktop koşar. Ders yuvasını (tools/ogrenme/onsoz.py) ~/.claude/agents/*.md ajan filosuna ekler.

  python onay/ruflo_1_uygula.py --kuru   # plan: hangi ajan değişir, kabul durumu (varsayılan)
  python onay/ruflo_1_uygula.py uygula   # yedek alır → frontmatter sonrası işaretli ders bloğu
  python onay/ruflo_1_uygula.py --geri   # işaretli bloğu söker (yedek ayrıca ~/.claude/yedek/ruflo1-*)
Kapı aile başına (kod/rapor/video, AILE önekleri): eşli A/B ≥4 çift, dersli ort. puan ≥ derssiz VE jeton < derssiz; yalnız geçen
ailenin ajanlarına eklenir. ders.py ana repoda (kol/ruflo main'e birleşmiş) olmalı. Yalnız gevşek ~/.claude/agents dosyaları; plugin ajanlarına, settings.json'a, hook'lara
dokunulmaz; `ruflo init` koşulmaz. MCP listesi önce=sonra değilse rc=1.
"""
import shutil
import statistics
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "onay"), str(KOK / "tools" / "ogrenme")]
from kalite_3_uygula import EV, mcp_var_mi  # noqa: E402
import onsoz  # noqa: E402

# d8: aile başına en yeni eşli ölçüm (v5 aynı (aile, sıra, kol) satırını v3'ün üstüne yazar; v4 yalnız dersliydi → düştü)
TSV = [KOK / "docs" / "kutuphane" / "olcum" / f"ruflo-1-ab-{v}-{a}.tsv" for v in ("v3", "v5") for a in ("kod", "rapor", "video")]
# Desktop 13 Eki d8: ders yuvası yalnız ölçütü geçen ailenin ajanlarına. ponytail: önek eşlemesi elle; yeni önek gelirse buraya.
AILE = {"kod": ("dn-", "dil-", "fe-", "db-", "qa-", "git-", "oyn-", "ml-", "otm-", "engineering-"), "rapor": ("dok-",), "video": ("vid-",)}


def kabul(tsv=TSV):
    """→ {aile: (geçti mi, açıklama)}. Yalnız iki kolu da koşmuş (aile, sıra) çiftleri, aile başına ≥4 çift;
    şart dersli ort. puan ≥ derssiz VE dersli toplam jeton (input+cache_creation+cache_read+output) < derssiz (Ömer: tabanın altına)."""
    try:
        # aile başına yalnız en yeni sürüm dosyası (v5'in eksik satırı v3'ten tamamlanıp karışık çift olmasın)
        son_dosya = {t.stem.rsplit("-", 1)[1]: t for t in ([] if isinstance(tsv, Path) else tsv) if t.exists()}
        satir = [s.split("\t") for t in ([tsv] if isinstance(tsv, Path) else son_dosya.values())
                 for s in t.read_text(encoding="utf-8").splitlines()[1:] if s.strip()]
    except OSError:
        satir = []
    son = {(s[1], s[2], s[3]): s for s in satir}  # aynı çift tekrar koştuysa son satır
    sonuc = {}
    for aile in AILE:
        cift = [(a, n) for a, n, k in son if a == aile and k == "derssiz" and (a, n, "dersli") in son]
        if len(cift) < 4:
            sonuc[aile] = (False, f"ölçüm eksik ({len(cift)}/4 çift)")
            continue
        ort = {k: statistics.mean(float(son[(a, n, k)][4]) for a, n in cift) for k in ("derssiz", "dersli")}
        jet = {k: sum(int(x) for a, n in cift for x in son[(a, n, k)][7:11]) for k in ("derssiz", "dersli")}
        sonuc[aile] = (ort["dersli"] >= ort["derssiz"] and jet["dersli"] < jet["derssiz"],
                       f"{len(cift)} çift · puan derssiz {ort['derssiz']:.3f} · dersli {ort['dersli']:.3f}"
                       f" · jeton {jet['dersli'] / jet['derssiz'] - 1:+.1%}")
    return sonuc


def ajanlar(ev=EV, aileler=AILE):
    onek = tuple(o for a in aileler for o in AILE[a])
    return sorted(f for f in (ev / ".claude" / "agents").glob("*.md") if f.name.startswith(onek))


def main(ev=EV, kip=None, tsv=TSV, ders_py=Path(onsoz.DERS_PY)):
    kip = kip or (sys.argv[1] if len(sys.argv) > 1 else "--kuru")
    once = mcp_var_mi(ev)
    k = kabul(tsv)
    acik = [a for a, (g, _) in k.items() if g]
    for a, (g, neden) in k.items():
        print(f"kabul {a}: {'GEÇTİ' if g else 'YOK'} ({neden})")
    print(f"ders.py: {'var' if ders_py.exists() else 'YOK (kol/ruflo main değil)'} · açık aileler: {', '.join(acik) or '-'}")
    if kip == "uygula":
        if not (acik and ders_py.exists()):
            print("uygulanmadı")
            return 1
        yedek = ev / ".claude" / "yedek" / f"ruflo1-{time.strftime('%Y%m%d-%H%M%S')}"
        yedek.mkdir(parents=True)
        n = 0
        for f in ajanlar(ev, acik):
            shutil.copy2(f, yedek / f.name)
            n += onsoz.enjekte(f)
        print(f"uygulandı {n} ajan · yedek {yedek}")
    elif kip == "--geri":
        print(f"geri alındı {sum(onsoz.enjekte(f, geri=True) for f in ajanlar(ev))} ajan")
    else:
        for f in ajanlar(ev, acik):
            print(f"{f.stem}\t{'eklenecek' if onsoz.enjekte(f, kuru=True) else 'aynı'}")
    ok = once == mcp_var_mi(ev)
    print("mcp önce=sonra" if ok else "HATA: MCP listesi değişti")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
