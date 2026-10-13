"""RUFLO-1 d11: kanca yargısının kalibrasyonu — gerçek alt ajan transkriptleri (~/.claude/projects/*/*/subagents) → kanca.yorunge
görünümü → Opus etiketi (başarı 0/1, ≤1 claude -p çağrısı, plan limiti) + Jev puanı (kanca._jev) → karma eşiği / test ödülü / güven payı
ızgara araması (dengeli doğruluk). Örnek metinleri yerelde kalır (.claude/ruflo11/); TSV'ye yalnız sayılar yazılır.
Ortak arayüz (LAYA-1): ornek.jsonl satırı = jev_yargic state'i {"gorev","yanit"} + "opus" etiketi → başka taşıyıcı aynı kümede ölçülür.
  python kalibre.py topla [N]   örnek + Opus + Jev → .claude/ruflo11/ornek.jsonl + docs/kutuphane/olcum/ruflo-1-kalibre.tsv
  python kalibre.py uydur       TSV → en iyi (ESIK, TEST_ODUL, PAY)"""
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
ETIKET = ("Aşağıda Claude Code alt ajan koşuları var (görev, araç/hata sayısı, son test sonucu, son araç çıktıları, son mesaj). "
          "Her koşu için: ajan görevi GERÇEKTEN başardı mı (istenen iş yapıldı, doğrulandı ya da doğrulanamadığı dürüstçe bildirildi "
          "ve iş yine de doğru)? basari 1/0, guven 0-1. Yalnız JSON liste: [{\"no\": n, \"basari\": 0|1, \"guven\": x}]\n\n%s")


def _son_ciktilar(yol, n=3):
    c = []
    for x in kanca._satirlar(yol, 512_000):
        for p in kanca._icerik(x):
            if p.get("type") == "tool_result":
                t = p.get("content")
                c.append(t if isinstance(t, str) else " ".join(y.get("text", "") for y in t or [] if isinstance(y, dict)))
    return [t[-300:] for t in c[-n:]]


def topla(n=60):
    yollar = sorted(Path.home().glob(".claude/projects/*/*/subagents/*.jsonl"))
    random.Random(11).shuffle(yollar)
    ornek = []
    for y in yollar:
        gorev, arac, hata, tur, son, test = kanca.yorunge(y)
        if arac >= kanca.EN_AZ_ARAC and son.strip() and gorev.strip():
            ornek.append({"gorev": gorev[:1500], "yanit": son[-1500:], "arac": arac, "hata": hata, "tur": tur, "test": test,
                          "ciktilar": _son_ciktilar(y)})
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
        o = kosucu.kos(ETIKET % metin, ek=["--strict-mcp-config", "--max-turns", "1"], model="opus", butce=1.0, timeout=600)
        usd += o["usd"]
        m = o["metin"]
        try:
            etiket |= {int(x["no"]): x for x in json.loads(m[m.index("["):m.rindex("]") + 1])}
        except ValueError as h:
            print("parti", b, "etiket okunamadı:", h, o["rc"], o["hata"], m[:200], flush=True)
    kayit.write_text(json.dumps(etiket, ensure_ascii=False), encoding="utf-8")
    sys.path.insert(0, str(kanca.KOK / "tools" / "jev"))
    from jev.cekirdek import Tasiyici
    jev = kanca._jev([{"gorev": x["gorev"], "yanit": x["yanit"]} for x in ornek], Tasiyici(en_fazla=5, istek_tavan=20))
    with open(YEREL / "ornek.jsonl", "w", encoding="utf-8") as f, open(TSV, "w", encoding="utf-8", newline="\n") as t:
        t.write("no\tarac\thata\ttest\tjev\topus\topus_guven\n")
        for i, (x, j) in enumerate(zip(ornek, jev), 1):
            e = etiket.get(i, {})
            x.update(jev=j, opus=e.get("basari"), opus_guven=e.get("guven"))
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
            t.write("\t".join(map(str, [i, x["arac"], x["hata"], x["test"], j, x["opus"], x["opus_guven"]])) + "\n")
    print(f"topla: {len(ornek)} örnek · opus ${usd:.3f} · etiket {len(etiket)} · jev {sum(j is not None for j in jev)}")


def _satirlar():
    import csv
    for r in csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"):
        if r["jev"] not in ("None", "") and r["opus"] not in ("None", ""):
            yield (float(r["jev"]), int(r["arac"]), int(r["hata"]), None if r["test"] == "None" else int(r["test"]), int(r["opus"]))


def uydur(satirlar=None):
    """→ (ESIK, TEST_ODUL, PAY, dengeli doğruluk, kapı içi doğruluk, kapsam). Eşitlikte küçük ödül (sade) kazanır."""
    s = list(satirlar if satirlar is not None else _satirlar())
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


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1] == "topla":
        topla(int(sys.argv[2]) if len(sys.argv) > 2 else 60)
    else:
        print("uydur: ESIK, TEST_ODUL, PAY, dengeli doğruluk, kapı içi doğruluk, kapsam =", uydur())
