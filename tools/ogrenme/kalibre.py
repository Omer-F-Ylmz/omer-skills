"""RUFLO-1 d11: kanca yargısının kalibrasyonu — gerçek alt ajan transkriptleri (~/.claude/projects/*/*/subagents) → kanca.yorunge
görünümü → Opus etiketi (başarı 0/1, ≤1 claude -p çağrısı, plan limiti) + Jev puanı (kanca._jev) → karma eşiği / test ödülü / güven payı
ızgara araması (dengeli doğruluk). Örnek metinleri yerelde kalır (.claude/ruflo11/); TSV'ye yalnız sayılar yazılır.
Ortak arayüz (LAYA-1): ornek.jsonl satırı = jev_yargic state'i {"gorev","yanit"} + "opus" etiketi → başka taşıyıcı aynı kümede ölçülür.
  python kalibre.py topla [N]   örnek + Opus + Jev → .claude/ruflo11/ornek.jsonl + docs/kutuphane/olcum/ruflo-1-kalibre.tsv
  python kalibre.py yargic [haiku|sonnet]   aynı örnekler → kanca._yargic puanı (TSV model sütunu)
  python kalibre.py uydur [jev|haiku|sonnet]   TSV → en iyi (ESIK, TEST_ODUL, PAY)"""
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kanca  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
YEREL = KOK / ".claude" / "ruflo11"
TSV = KOK / "docs" / "kutuphane" / "olcum" / "ruflo-1-kalibre.tsv"
def topla(n=60):
    yollar = sorted(Path.home().glob(".claude/projects/*/*/subagents/*.jsonl"))
    random.Random(11).shuffle(yollar)
    ornek = []
    for y in yollar:
        gorev, arac, hata, tur, son, test = kanca.yorunge(y)
        if arac >= kanca.EN_AZ_ARAC and son.strip() and gorev.strip():
            ornek.append({"gorev": gorev[:1500], "yanit": son[-1500:], "arac": arac, "hata": hata, "tur": tur, "test": test,
                          "ciktilar": kanca.son_ciktilar(y)})
        if len(ornek) == n:
            break
    sys.path.insert(0, str(KOK / "tools" / "olcum"))
    os.environ.pop("ANTHROPIC_API_KEY", None)  # plan limiti
    os.environ["OGRENME_KANCA"] = "0"
    import kosucu
    YEREL.mkdir(parents=True, exist_ok=True)
    kayit = YEREL / "opus.json"  # Jev adımı düşerse Opus yeniden çağrılmaz
    etiket = {int(k): v for k, v in json.loads(kayit.read_text(encoding="utf-8")).items()} if kayit.exists() else {}
    usd = 0.0
    for b in range(0, len(ornek), 12) if not etiket else ():  # istem argv'de (Windows ~32k karakter) → 12'lik parti, ≤5 Opus çağrısı
        metin = "\n\n".join(f"Koşu {i}: {o['arac']} araç · {o['hata']} hata · test {o['test']}\nGörev: {o['gorev'][:500]}\n"
                            f"Son çıktılar: {' | '.join(t[-200:] for t in o['ciktilar'])}\nSon mesaj: {o['yanit'][-500:]}"
                            for i, o in enumerate(ornek[b:b + 12], b + 1))
        o = kosucu.kos(kanca.ETIKET % metin, ek=["--strict-mcp-config", "--max-turns", "1"], model="opus", butce=1.0, timeout=600)
        usd += o["usd"]
        m = o["metin"]
        try:
            etiket |= {int(x["no"]): x for x in json.loads(m[m.index("["):m.rindex("]") + 1])}
        except ValueError as h:
            print("parti", b, "etiket okunamadı:", h, o["rc"], o["hata"], m[:200], flush=True)
    kayit.write_text(json.dumps(etiket, ensure_ascii=False), encoding="utf-8")
    sys.path.insert(0, str(kanca.KOK / "tools" / "jev"))
    from jev.cekirdek import Tasiyici
    jev = kanca._jev([{"gorev": x["gorev"], "yanit": x["yanit"]} for x in ornek], Tasiyici(en_fazla=5, istek_tavan=80))  # API arka ucu state başına 1 istek (60 → ~50) + tekrar payı
    with open(YEREL / "ornek.jsonl", "w", encoding="utf-8") as f, open(TSV, "w", encoding="utf-8", newline="\n") as t:
        t.write("no\tarac\thata\ttest\tjev\topus\topus_guven\n")
        for i, (x, j) in enumerate(zip(ornek, jev), 1):
            e = etiket.get(i, {})
            x.update(jev=j, opus=e.get("basari"), opus_guven=e.get("guven"))
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
            t.write("\t".join(map(str, [i, x["arac"], x["hata"], x["test"], j, x["opus"], x["opus_guven"]])) + "\n")
    print(f"topla: {len(ornek)} örnek · opus ${usd:.3f} · etiket {len(etiket)} · jev {sum(j is not None for j in jev)}")


def yargic(sutun="haiku"):
    """Aynı örnekler → kanca._haiku (kancanın varsayılan yargıcı; 12'lik parti, ≤5 haiku çağrısı) → TSV'ye haiku sütunu."""
    import csv
    ornek = [json.loads(x) for x in open(YEREL / "ornek.jsonl", encoding="utf-8")]
    puan = []
    for b in range(0, len(ornek), 12):
        try:
            puan += kanca._yargic(ornek[b:b + 12], sutun)
        except ValueError as h:
            print("parti", b, "okunamadı:", h, flush=True)
            puan += [None] * len(ornek[b:b + 12])
    r = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
    alan = [k for k in r[0] if k != sutun] + [sutun]
    with open(TSV, "w", encoding="utf-8", newline="\n") as t:
        t.write("\t".join(alan) + "\n")
        for x, p in zip(r, puan):
            t.write("\t".join([x[k] for k in alan[:-1]] + [str(p)]) + "\n")
    print(f"{sutun}: {sum(p is not None for p in puan)}/{len(ornek)} puan")


def _satirlar(sutun="jev"):
    import csv
    for r in csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"):
        if r.get(sutun) not in (None, "None", "") and r["opus"] not in ("None", ""):
            yield (float(r[sutun]), int(r["arac"]), int(r["hata"]), None if r["test"] == "None" else int(r["test"]), int(r["opus"]))


def uydur(satirlar=None, sutun="jev"):
    """→ (ESIK, TEST_ODUL, PAY, dengeli doğruluk, kapı içi doğruluk, kapsam). Eşitlikte küçük ödül (sade) kazanır."""
    s = list(satirlar if satirlar is not None else _satirlar(sutun))
    en = None
    for odul in (0, 1, 2, 3, 4):
        k = [(kanca.karma(j, a, h, "x", t, odul), y) for j, a, h, t, y in s]
        for e10 in range(20, 85, 5):
            e = e10 / 10
            dogru = [sum((km >= e) == bool(y) for km, y in k if y == c) / max(1, sum(y == c for _, y in k)) for c in (0, 1)]
            bd = sum(dogru) / 2
            if en is None or bd > en[3] + 1e-9:
                en = (e, odul, None, bd)
    e, odul, _, bd = en
    k = [(kanca.karma(j, a, h, "x", t, odul), y) for j, a, h, t, y in s]
    for p10 in range(0, 45, 5):  # güven payı: |karma − eşik| ≥ PAY olan koşulardan ders; kapı içi doğruluk ≥ 0.9 ilk pay
        ic = [(km >= e) == bool(y) for km, y in k if abs(km - e) >= p10 / 10]
        if ic and sum(ic) / len(ic) >= 0.9:
            return e, odul, p10 / 10, round(bd, 3), round(sum(ic) / len(ic), 3), round(len(ic) / len(k), 3)
    return e, odul, None, round(bd, 3), None, 0.0


def _kayit(y, kaynak, aile, nesnel):
    gorev, arac, hata, tur, son, test = kanca.yorunge(y)
    if arac and (son.strip() or kaynak == "yarim") and gorev.strip():  # isle her bitti yörüngesini yargılar (EN_AZ_ARAC yalnız damıtma); kesilen koşunun son mesajı boştur
        return {"kaynak": kaynak, "aile": aile, "gorev": gorev[:1500], "son": son[-1500:], "arac": arac, "hata": hata, "tur": tur,
                "test": test, "ciktilar": kanca.son_ciktilar(y), "nesnel": nesnel}


def zor_kume(en_fazla=60):
    """d13: nesnel etiketli küme (≥20 başarısız). gercek = e2e görev klasörü ab_olc.yargic ile yeniden puanlanır (1.0 → başarı);
    yarim = başarılı koşunun ilk Edit/Write'tan önce kesilmiş transkripti (teslim dosyası kur() hâli → yargic < 1.0, başarısız);
    opus = ornek.jsonl'deki Opus başarısızları (nesnel değil, ayrı raporlanır)."""
    import re
    import tempfile
    sys.path.insert(0, str(KOK / "tools" / "olcum"))
    import ab_olc
    gercek, yarim, tmp = [], [], Path(tempfile.mkdtemp(prefix="ruflo13-"))
    for d in sorted(Path(tempfile.gettempdir()).glob("ruflo-kanca-*")):
        m = re.match(r"ruflo-kanca-(?:(rapor)-)?(\d+)-", d.name)
        if not m:
            continue
        aile, i = m[1] or "kod", int(m[2])
        nesnel = int(ab_olc.yargic(aile, i, d)[0] == 1.0)
        for y in Path.home().glob(".claude/projects/" + re.sub(r"[^A-Za-z0-9]", "-", str(d)) + "/*/subagents/*.jsonl"):
            if k := _kayit(y, "gercek", aile, nesnel):
                gercek.append(k)
            satir = y.read_text(encoding="utf-8", errors="replace").splitlines()
            kes = next((n for n, s in enumerate(satir) if '"name":"Edit"' in s.replace(" ", "") or '"name":"Write"' in s.replace(" ", "")), None)
            if nesnel and kes:
                p = tmp / f"{d.name}-{y.stem}.jsonl"
                p.write_text("\n".join(satir[:kes]), encoding="utf-8")
                if k := _kayit(p, "yarim", aile, 0):
                    yarim.append(k)
    opus = [dict(x, kaynak="opus", aile="?", son=x["yanit"], nesnel=0) for x in map(json.loads, open(YEREL / "ornek.jsonl", encoding="utf-8"))
            if x.get("opus") == 0]
    basarisiz = [k for k in gercek if not k["nesnel"]] + opus
    random.Random(13).shuffle(yarim)
    basarisiz += yarim[:max(20 - len(basarisiz), (en_fazla - len(basarisiz)) // 2)]
    basarili = [k for k in gercek if k["nesnel"]]
    random.Random(13).shuffle(basarili)
    kume = basarisiz + basarili[:en_fazla - len(basarisiz)]
    random.Random(13).shuffle(kume)
    return kume


def zor(model="sonnet"):
    """Küme → kanca._yargic (12'lik parti, ≤5 çağrı) → karma(ESIK) ile kaynak başına doğruluk; TSV ruflo-1-kalibre-zor.tsv."""
    os.environ.pop("ANTHROPIC_API_KEY", None)
    os.environ["OGRENME_KANCA"] = "0"
    kume = zor_kume()
    print("küme:", len(kume), {s: sum(k["kaynak"] == s and not k["nesnel"] for k in kume) for s in ("gercek", "yarim", "opus")}, "başarısız ·",
          sum(k["nesnel"] for k in kume), "başarılı", flush=True)
    puan = []
    for b in range(0, len(kume), 12):
        try:
            puan += kanca._yargic(kume[b:b + 12], model)
        except ValueError as h:
            print("parti", b, "okunamadı:", h, flush=True)
            puan += [None] * len(kume[b:b + 12])
    with open(TSV.with_name("ruflo-1-kalibre-zor.tsv"), "w", encoding="utf-8", newline="\n") as t:
        t.write(f"no\tkaynak\taile\tarac\thata\ttest\tnesnel\t{model}\tkarma\n")
        for n, (k, j) in enumerate(zip(kume, puan), 1):
            km = None if j is None else kanca.karma(j, k["arac"], k["hata"], "x", k["test"])
            k["karma"] = km
            t.write("\t".join(map(str, [n, k["kaynak"], k["aile"], k["arac"], k["hata"], k["test"], k["nesnel"], j, km])) + "\n")
    for s in ("gercek", "yarim", "opus", "hepsi"):
        for c in (0, 1):
            g = [k for k in kume if k.get("karma") is not None and k["nesnel"] == c and s in ("hepsi", k["kaynak"])]
            if g:
                print(f"{s} {'başarısız' if c == 0 else 'başarılı'}: {sum((k['karma'] >= kanca.ESIK) == bool(c) for k in g)}/{len(g)} doğru", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1] == "zor":
        zor(*sys.argv[2:3])
    elif sys.argv[1] == "topla":
        topla(int(sys.argv[2]) if len(sys.argv) > 2 else 60)
    elif sys.argv[1] == "yargic":
        yargic(sys.argv[2] if len(sys.argv) > 2 else "haiku")
    else:
        print("uydur: ESIK, TEST_ODUL, PAY, dengeli doğruluk, kapı içi doğruluk, kapsam =", uydur(sutun=sys.argv[2] if len(sys.argv) > 2 else "jev"))
