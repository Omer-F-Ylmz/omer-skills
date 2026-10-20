"""BEYIN-4 d2 kapı: tohum 2009+2010 (sayısal) + 2011 (sayısal olmayan, çok notlu; sorular-<tohum>.jsonl, betik üretimi), A = `beyin.py ara`, B = yalnız Read; düzenek beyin2/kapi.py.
Hakem: sayısalda BETİK (cevaptaki her sayı aday cevapta tam geçerse doğru); sayısal olmayanda iki ailenin ücretsiz bulut modeli (OmniRoute :free), iki ayrı doğruluk. Ölçü: doğruluk + API girdi token'ı A/B.
Kullanım: python .claude/beyin4/kapi.py [adım...]  (adım: A2009 B2009 A2010 B2010 A2011 B2011; varsayılan hepsi; kosu/<adım>.json varsa yeniden kullanılır)
Kabul: doğruluk ≥%92 ve token A ≤ B'nin %25."""
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).parent
sys.path.insert(0, str(D.parent / "beyin2"))
import kapi  # noqa: E402

kapi.CIKTI = D / "kosu"
kapi.CIKTI.mkdir(exist_ok=True)
TOHUM = (2009, 2010, 2011)
SAYISAL = (2009, 2010)
sys.path.insert(0, str(D.parent.parent / "tools"))
import ucuz_alt  # noqa: E402
# iki ayrı aile; her biri için :free yedek zinciri (429 → sıradaki / bekle)
AILE = {"nvidia": ["openrouter/nvidia/nemotron-3.5-lightning:free", "openrouter/nvidia/nemotron-3-super-120b-a12b:free", "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"],
        "google": ["openrouter/google/gemma-4-31b-it:free", "openrouter/google/gemma-4-26b-a4b-it:free"]}
HAKEM = ("Her satırda soru, referans (doğru değer/değerler) ve aday cevap var. Aday, referanstaki HER değeri (ad/yol/kimlik/kelime) doğru veriyorsa d=1, "
         "eksik ya da yanlışsa d=0 (yol biçimi farkı: \\ ile / aynıdır). Yalnız satır başına bir JSON yaz: {\"id\":N,\"d\":0|1}.\n")
S = {t: [json.loads(s) for s in (D / f"sorular-{t}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()] for t in TOHUM}


def liste(t):
    return "\n".join(f'{q["id"]}. {q["soru"]}' for q in S[t])


def calis(ad, istem, arac=None, izin=None, tur=None):
    yol = kapi.CIKTI / f"{ad}.json"
    return json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else kapi.cagir(ad, istem, arac, izin, tur)


def dogru(q, cevap):
    return all(re.search(rf"(?<![\d.,]){re.escape(s)}(?!\d)", str(cevap)) for s in q["cevap"].split(";") if s.strip())


def llm_hakem(aile, t, cev):
    """{id: 0|1}; kosu/hakem-<aile>-<t>.json önbellek. 429/boş → zincirde sıradaki model, 10 tur."""
    yol = kapi.CIKTI / f"hakem-{aile}-{t}.json"
    if yol.exists():
        return {int(k): v for k, v in json.loads(yol.read_text(encoding="utf-8")).items()}
    istem = HAKEM + "\n".join(json.dumps({"id": q["id"], "soru": q["soru"], "referans": q["cevap"], "aday": str(cev.get(q["id"], ""))},
                                         ensure_ascii=False) for q in S[t])
    for i in range(10):
        try:
            y = ucuz_alt.sor("omni", AILE[aile][i % len(AILE[aile])], {"messages": [{"role": "user", "content": istem}], "max_tokens": 8000})[0]
        except Exception as e:  # noqa: BLE001
            print(f"hakem {aile} {t} deneme {i}: {e}", file=sys.stderr)
            time.sleep(30)
            continue
        d = {int(a): int(b) for a, b in re.findall(r'"id"\s*:\s*(\d+)\s*,\s*"d"\s*:\s*([01])', y)}
        if set(d) >= {q["id"] for q in S[t]}:
            yol.write_text(json.dumps(d), encoding="utf-8")
            return d
    return {}


def main():
    isler = {}
    for t in TOHUM:
        isler[f"A{t}"] = (kapi.CEVAP_A + liste(t), "Bash", f"Bash({kapi.BEYIN_KOMUT}:*)", kapi.TUR)
        isler[f"B{t}"] = (kapi.CEVAP_B + liste(t), "Read", None, kapi.TUR)
    ad = sys.argv[1:] or list(isler)
    with ThreadPoolExecutor(6) as ex:
        sonuc = dict(zip(ad, ex.map(lambda k: calis(k, *isler[k]), ad)))
    rapor = []
    for t in TOHUM:
        for kol in "AB":
            if f"{kol}{t}" in sonuc:
                cev = {c.get("id"): c.get("cevap") for c in kapi.satirlar(sonuc[f"{kol}{t}"])}
                if t in SAYISAL:
                    ds = {"betik": {q["id"]: dogru(q, cev.get(q["id"], "")) for q in S[t]}}
                elif kol == "A":
                    ds = {a: llm_hakem(a, t, cev) for a in AILE}
                else:
                    continue
                for h, d in ds.items():
                    if not d:  # hakem hiç yanıt vermedi (429) → 0/20 doğruluk gibi görünmesin
                        rapor.append(f"tohum {t} {kol} hakem {h}: YOK (429)")
                        continue
                    rapor.append(f"tohum {t} {kol} hakem {h}: {sum(d.get(q['id'], 0) for q in S[t])}/{len(S[t])}"
                                 f" (çok {sum(d.get(q['id'], 0) for q in S[t] if q['cok'])}/{sum(q['cok'] for q in S[t])})"
                                 f" yanlış {[q['id'] for q in S[t] if not d.get(q['id'])]}")
        if f"A{t}" in sonuc and f"B{t}" in sonuc:
            a, b = sonuc[f"A{t}"], sonuc[f"B{t}"]
            rapor.append(f"tohum {t}: token A {kapi.girdi(a)} B {kapi.girdi(b)} = %{100 * kapi.girdi(a) / max(1, kapi.girdi(b)):.0f}"
                         f" tur A {a.get('num_turns')} B {b.get('num_turns')} ihlal A {kapi.ihlal(a)}")
    (kapi.CIKTI / "sonuc.txt").write_text("\n".join(rapor), encoding="utf-8")
    print("\n".join(rapor))


if __name__ == "__main__":
    main()
