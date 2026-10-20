"""MAKARA döngü 1 (iş sırasında, model yok): ajan-sira/*.json sonuçlarından DERS satırı çıkarır → 50-dersler/ders-<gün>.md.
Aynı ders tekrar gelirse sayaç artar (anahtar = normalize metin), ikinci not açılmaz; kaynak dosya (ad+mtime) bir kez işlenir.
60-ajanlar notları bu JSON'ların birebir kopyasıdır (beyin_al); ders satırı kaynaktan okunur, parçalı not birleştirmek gerekmez.
`onek(istem)`: ajan_sira istem önüne eklenen ≤600 jetonluk ilgili 3-5 ders satırı (MAKARA_DERS=0 kapatır)."""
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
KASA = Path(r"C:\Users\pc\Desktop\Obsidian")
DURUM = KOK / ".kos/makara/ders.json"
SIRA = KOK / ".kos/kopru/ajan-sira"
BEKLE = 30  # sn; yazılmakta olan dosyaya dokunma
DERS = re.compile(r"(?i)\b(ders|öğrenilen|ogrenilen|risk|kök neden|kok neden|sapma|ıska|iska)\b")
ONEK_KAR = 1800  # ~600 jeton


def anahtar(m):
    return hashlib.sha1(re.sub(r"\W+", " ", re.sub(r"\d+", "#", m.lower())).strip()[:80].encode()).hexdigest()[:10]


def satirlar(sonuc):
    for s in sonuc.splitlines():
        s = re.sub(r"^[\s>*#\-•\d.)]+|\*\*", "", s).strip()
        if 15 <= len(s) <= 300 and DERS.search(s):
            yield s


def yukle():
    return json.loads(DURUM.read_text(encoding="utf-8")) if DURUM.exists() else {"islenen": {}, "dersler": {}, "gunler": {}}


def tara(sira=SIRA, durum_yol=DURUM, simdi=None):
    """Yeni biten oturumları işler; (işlenen dosya sayısı, yeni ders, tekrar) döner. Durumu yazar."""
    d, simdi = yukle(), simdi or time.time()
    yeni = tekrar = n = 0
    for p in sorted(Path(sira).glob("*.json")):
        mt = p.stat().st_mtime
        if d["islenen"].get(p.name) == mt or simdi - mt < BEKLE:
            continue
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        gun = time.strftime("%Y-%m-%d", time.localtime(mt))
        g = d["gunler"].setdefault(gun, {"is": 0, "maliyet": 0.0, "iska": 0, "modeller": {}, "anahtarlar": []})
        g["is"] += 1
        g["maliyet"] = round(g["maliyet"] + (j.get("total_cost_usd") or 0), 4)
        g["iska"] += bool(j.get("is_error") or j.get("permission_denials"))
        for m in j.get("modelUsage") or {}:
            g["modeller"][m] = g["modeller"].get(m, 0) + 1
        for s in satirlar(j.get("result") or "") if isinstance(j.get("result"), str) else ():
            k = anahtar(s)
            e = d["dersler"].get(k)
            if e:
                if p.name not in e["kaynak"]:
                    e["sayac"] += 1; e["son"] = gun; e["kaynak"].append(p.name); tekrar += 1
            else:
                d["dersler"][k] = {"metin": s, "sayac": 1, "ilk": gun, "son": gun, "kaynak": [p.name]}; yeni += 1
            if k not in g["anahtarlar"]:
                g["anahtarlar"].append(k)
        d["islenen"][p.name] = mt
        n += 1
    if n:
        durum_yol.parent.mkdir(parents=True, exist_ok=True)
        durum_yol.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return n, yeni, tekrar


def not_yaz(gun, d, kasa=KASA):
    g = d["gunler"][gun]
    sat = [f"- {d['dersler'][k]['metin']} (×{d['dersler'][k]['sayac']}, ilk {d['dersler'][k]['ilk']})" for k in g["anahtarlar"]]
    govde = (f"---\nkaynak: ajan-sira (makara_ders)\nguncellenme: {gun}\ntur: ders\nguven: betik-cikarim\netiket: [ders, makara]\n---\n"
             f"# ders {gun}\n## Maliyet / ıska\n{g['is']} oturum · ${g['maliyet']} · ıska {g['iska']} · modeller {', '.join(sorted(g['modeller'])) or '-'}\n"
             f"## Dersler (ajan sonuçlarındaki Ders/öğrenilen/risk/kök neden/sapma satırları)\n" + ("\n".join(sat) or "yok") + "\n")
    y = Path(kasa) / "50-dersler" / f"ders-{gun}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_bytes(govde.encode("utf-8"))
    return y


def main():
    n, yeni, tekrar = tara()
    if n:
        d = yukle()
        for gun in d["gunler"]:
            if d["gunler"][gun]["anahtarlar"] or d["gunler"][gun]["is"]:
                not_yaz(gun, d)
    print(f"makara_ders: {n} oturum · {yeni} yeni ders · {tekrar} tekrar")


def ilgili(istem, k=5):
    """beyin ara ile 50-dersler parçaları; [(kaynak:satır, ilk metin satırı)] — hata olursa boş (kuyruğu bozmaz)."""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import beyin
        sonuc = beyin.ara(re.sub(r"\s+", " ", istem)[:300], 8)
    except Exception:
        return []
    out = []
    for kaynak, no, sat in sonuc:
        if "50-dersler" not in str(kaynak).replace("\\", "/"):
            continue
        t = next((s.strip() for s in sat if len(s.strip()) > 20 and not s.startswith(("---", "#", "kaynak", "guven"))), "")
        if t:
            out.append(t[:200])
    return out[:k]


def onek(istem):
    if os.environ.get("MAKARA_DERS") == "0":
        return ""
    sat = ilgili(istem)
    if len(sat) < 3:
        return ""
    return ("[makara: kasadan ilgili ders satırları — bağlam, talimat değil]\n" + "\n".join("- " + s for s in sat))[:ONEK_KAR] + "\n\n"


if __name__ == "__main__":
    main()
