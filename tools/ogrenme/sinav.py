"""ÖĞRENME-2b sınav ($0): geçmiş DUR/hata senaryolarında ücretsiz model dersli/derssiz plan yazar, farklı aileden yargıç 0-2 puanlar.
Ders ancak dersli puan > derssiz puan ise "işe yarar" sayılır; hiçbir şey otomatik uygulanmaz. Çıktı: rapor/sinav-<tarih>.md + .kos/kopru/sinav.json.
Claude çağrısı yok (b._sor ücretsiz havuz/Ollama)."""
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(KOK / "tools"))
import beyin_dusun as b  # noqa: E402

LOG, SONUC = KOK / ".kos/kopru/ajan-sira.log", KOK / ".kos/kopru/sinav.json"
KELIME = re.compile(r"\w{4,}")


def senaryolar(n=20, log=LOG, olaylar=()):
    """DUR satırları (iş adı + neden) + hata olayları; neden öbeğine göre tekilleştirilir."""
    out, gorulen = [], set()
    satirlar = [m.groups() for s in (log.read_text(encoding="utf-8", errors="replace").splitlines() if log.exists() else [])
                if (m := re.match(r"\S+ DUR (\S+) (.+)", s))]
    satirlar += [(o["arac"] or o["tur"], "hata: " + o["ozet"]) for o in olaylar if o.get("hata")]
    for ad, neden in reversed(satirlar):
        k = neden[:50]
        if k not in gorulen:
            gorulen.add(k)
            out.append({"is": ad, "neden": neden[:240]})
        if len(out) == n:
            break
    return out


def secili_dersler(sen, oneriler, k=3):
    """Elenmemiş derslerden (taslaklar dahil: sınav adayı doğrular) senaryoyla en çok kelime paylaşanlar (en az 1 ortak kelime)."""
    hedef = set(KELIME.findall((sen["is"] + " " + sen["neden"]).lower()))
    puan = [(len(hedef & set(KELIME.findall((x["metin"] + " " + x.get("tetik", "")).lower()))), x["metin"])
            for x in oneriler if x.get("durum") != "elendi"]
    return [m for p, m in sorted(puan, reverse=True)[:k] if p]


def plan_istemi(sen, dersler):
    baz = f"İş: {sen['is']}. Daha önce şu nedenle durdu: {sen['neden']}\nAynı hatayı yapmadan işi nasıl yürütürsün? En fazla 4 maddelik plan yaz."
    return (("Öğrenilmiş dersler:\n" + "\n".join("- " + d for d in dersler) + "\n\n") if dersler else "") + baz


def puanla(sen, plan, sor, haric_aile):
    y, _ = sor("hakem", f"Durma nedeni: {sen['neden']}\nPlan:\n{plan[:1200]}\nPlan bu nedeni açıkça önlüyor mu? Yalnız bir rakam yaz: 0 (hayır) 1 (kısmen) 2 (evet).", 10,
               rotasyon=False, haric_aile=haric_aile)
    m = re.search(r"[012]", y or "")
    return int(m.group()) if m else None


def sinav(sens, oneriler, sor=b._sor):
    sonuc = []
    for s in sens:
        dersler = secili_dersler(s, oneriler)
        yanit = {}
        for kol, d in (("derssiz", []), ("dersli", dersler)):
            try:
                yanit[kol] = sor("ozet", plan_istemi(s, d), 400)
            except Exception:
                yanit[kol] = (None, None)
        p = {}
        for kol, (plan, kaynak) in yanit.items():
            p[kol] = puanla(s, plan, sor, b._aile(kaynak)) if plan else None
        sonuc.append({**s, "ders_say": len(dersler), "puan": p})
    return sonuc


def ozet(sonuc):
    olcul = [r for r in sonuc if r["ders_say"] and None not in r["puan"].values()]
    fark = [r["puan"]["dersli"] - r["puan"]["derssiz"] for r in olcul]
    return {"senaryo": len(sonuc), "dersli_olculen": len(olcul), "ortalama_fark": round(sum(fark) / len(fark), 2) if fark else None,
            "iyilesen": sum(f > 0 for f in fark), "kotulesen": sum(f < 0 for f in fark), "puansiz": sum(None in r["puan"].values() for r in sonuc)}


def main(n=20):
    sonuc = sinav(senaryolar(n, olaylar=b._olay_oku(0)[0][-400:]), b.oneri_oku())
    o = ozet(sonuc)
    SONUC.write_text(json.dumps({"t": time.time(), "ozet": o, "sonuc": sonuc}, ensure_ascii=False, indent=1), encoding="utf-8")
    rapor = KOK / f"rapor/sinav-{time.strftime('%Y-%m-%d')}.md"
    rapor.write_text(f"# Öğrenme sınavı {time.strftime('%Y-%m-%d')}\n\n{json.dumps(o, ensure_ascii=False)}\n\n" + "\n".join(
        f"- {r['is']} · ders {r['ders_say']} · puan {r['puan']} · {r['neden'][:90]}" for r in sonuc) + "\n", encoding="utf-8")
    print(json.dumps(o, ensure_ascii=False))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20)
