"""BEYIN-3 d2 tohum üretimi: tek Sonnet (claude -p) tohum başına 20 soru + kaynak satırlı cevap anahtarı.
d1'in 40 sorusunun kaynak dosyaları yasak; iki tohum dosya adı a–l / m–z diye bölünür. Çıktı: sorular-<tohum>.jsonl
Kullanım: python .claude/beyin3/uret.py   (2 ücretsiz abonelik çağrısı)"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "beyin2"))
import kapi  # noqa: E402

D = Path(__file__).parent
kapi.CIKTI = D / "kosu"
kapi.CIKTI.mkdir(exist_ok=True)
ESKI = [json.loads(s) for s in (D.parent / "beyin2/sorular.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
YASAK = sorted({re.sub(r":\d+$", "", k.strip()).split("/")[-1] for q in ESKI for k in q["kaynak"].split(";")})
BOLGE = {2007: ("a–l", "ilk yarısı (1–114. satır)", 200), 2008: ("m–z", "ikinci yarısı (115–229. satır)", 300)}

ISTEM = """Bir bilgi tabanı sınaması için {n} soru + cevap anahtarı üret (tohum {tohum}). Yalnız Read/Grep/Glob kullan.
Kaynaklar: C:\\Projeler\\omer-skills\\.kos\\kopru\\ajan-sira\\*.json (her dosyada tek satır JSON; "result" alanı), .kos\\kopru\\gorev\\*.md,
.kos\\kopru\\gorev-gecmis\\*.md, .kos\\kopru\\devir\\*.md, docs\\ogren\\*.md, docs\\kurulumlar\\*.md, C:\\Projeler\\omer-kurallar.md,
~/.claude/projects/C--Projeler-omer-skills/memory/*.md, .kos\\kopru\\SIRA.md.
Bölge: yalnız dosya adı {harf} aralığında başlayan dosyalar; SIRA.md'de yalnız {sira}.
Yasak dosyalar (başka sınamada kullanıldı; bunlardan soru üretme): {yasak}. Ayrıca tools/, tests/, .claude/ ve rapor/beyin-* kaynak olmasın.
Kurallar:
- Her soru tek somut olguyu sorar (sayı, ad, karar, sınır, neden); doğal Türkçe; cevabın sözcüklerini soruya kopyalama. Soru, hangi görev/not
  olduğunu sezdiren bir ad ya da ID içersin (örn. görev adı) — ama cevap değil.
- En az 8 soru "cok": true — cevap iki AYRI parçadan oluşur ve parçalar iki farklı dosyada (örn. görev tanımı + ajan-sira sonucu) geçer.
- En az 6 soru kaynağı ajan-sira/*.json ya da SIRA.md olsun.
- Her cevap anahtarının kaynağını Read ile DOĞRULA; kaynak "tamyol:satır" (cok için "yol:satır; yol:satır"). Cevap kısa (≤25 kelime).
- Soruların hiçbiri diğeriyle aynı olguyu sormasın; en az 12 farklı kaynak dosya kullan.
Çıktı: YALNIZ JSONL, {n} satır: {{"id":{ilk},"soru":"…","cevap":"…","kaynak":"…","cok":true|false}} (id {ilk}'den artarak).
"""


def uret(tohum):
    harf, sira, ilk = BOLGE[tohum]
    r = kapi.cagir(f"uret{tohum}", ISTEM.format(n=20, tohum=tohum, harf=harf, sira=sira, ilk=ilk + 1,
                                               yasak=", ".join(YASAK)), "Read,Grep,Glob", None, "60")
    out = [q for q in kapi.satirlar(r) if q.get("soru") and q.get("cevap") and q.get("kaynak")]
    (D / f"sorular-{tohum}.jsonl").write_text("\n".join(json.dumps(q, ensure_ascii=False) for q in out) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    with ThreadPoolExecutor(2) as ex:
        for t, o in zip(BOLGE, ex.map(uret, BOLGE)):
            print(t, len(o), "çok", sum(bool(q.get("cok")) for q in o))
