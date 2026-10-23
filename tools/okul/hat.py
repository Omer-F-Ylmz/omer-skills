"""USTA-OKULU-0 üretim hattı: kaynak toplama -> ücretsiz özet (A) -> ücretsiz çelişki/doğruluk (B) + alıntı denetimi -> Obsidian 30-okul/<alan>/ + docs/okul/.
Claude YOK: tüm model çağrıları tools/ucuz_alt.py (yalnız :free/ollama). Alıntı denetimi ($0) betikte.
  python tools/okul/hat.py <alan> [--kuru]       kaynak: docs/okul/kaynak/<alan>/*.md|*.txt (internet taraması çıktısı buraya konur)
Çıkış: 0 doğrulandı · 2 kaynak yok · 3 alıntı/çelişki denetimi geçmedi (taslak yazıldı, ders kitabına GİRMEZ) · 5 ücretsiz yol yok (bekle)"""
import json, os, re, subprocess, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KASA = Path(r"C:\Users\pc\Desktop\Obsidian")
alan = sys.argv[1]
kuru = "--kuru" in sys.argv
a = json.loads(Path(__file__).with_name("alanlar.json").read_text(encoding="utf-8"))[alan]
kaynak = sorted(p for p in (KOK / f"docs/okul/kaynak/{alan}").glob("*") if p.suffix in (".md", ".txt"))
if not kaynak:
    print(f"kaynak yok: docs/okul/kaynak/{alan}/ (önce geniş tarama çıktısını koy)"); sys.exit(2)
ara = KOK / f".kos/kopru/ara/okul"; ara.mkdir(parents=True, exist_ok=True)
istem0 = istem = (Path(__file__).with_name("sablon.md").read_text(encoding="utf-8")).format(ad=a["ad"], proje=a["proje"])
A, B = ara / f"{alan}-A.md", ara / f"{alan}-B.md"
print(f"{alan}: {len(kaynak)} kaynak"); 
if kuru: print("kuru: model çağrılmadı"); sys.exit(0)

sys.path.insert(0, str(KOK / "tools")); import ucretsiz_havuz
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[*`]", "", s)).strip().lower()  # biçim süsü (**, `) sayılmaz; sözcükler birebir
bag = {p.name: norm(p.read_text(encoding="utf-8", errors="replace")) for p in kaynak}
baglam = "".join(f'\n\n<dosya adi="{p.name}">\n{p.read_text(encoding="utf-8", errors="replace")}\n</dosya>' for p in kaynak)
ALINTI = re.compile(r'^> "(.+?)" \(([\w.\-]+\.md)\)', re.M)

def kontrol(m):
    # kök neden: ucuz_alt `ozet` türü JSON {ozet, alinti[1-3]} şeması dayatıyor -> kitap kısa özete düşüyor, madde başına alıntı çıkmıyor. Serbest metin + alıntı denetimi burada.
    bul = ALINTI.findall(m)
    kotu = [q for q, d in bul if d not in bag or norm(q) not in bag[d]]
    return None if bul and not kotu else (f"{len(kotu)} alıntı kaynakta birebir yok: {kotu[0][:60]!r}" if kotu else "alıntı yok")

def suz(m):
    """alıntısı kaynakta birebir tutmayan maddeyi at (küçük modeller alıntıyı bozuyor); **kalın**/`kod` süsünü kanonik biçime çevir"""
    iyi = []
    for b in re.split(r"(?m)^(?=> )", m):
        r = re.match(r'> \**"(.+?)"\**\s*\(`?([\w.\-]+\.md)`?\)[^\n]*\n?(.*)', b.strip(), re.S)
        if r and r.group(2) in bag and norm(r.group(1)) in bag[r.group(2)]:
            iyi.append(f'> "{r.group(1)}" ({r.group(2)})\n{r.group(3).strip()}'.strip())
    return iyi

def yaz(bolum):
    istem = (f"{istem0}\nYALNIZ şu bölümü yaz: {bolum}. Her madde `> \"birebir alıntı\" (dosya.md)` satırıyla başlar (dosya = <dosya adi>), altında tek satır Türkçe yorum: yorum yalnız alıntının çevirisi/özeti olsun; kaynakta olmayan hata senaryosu, sürüm, sayı, neden EKLEME. 6-10 madde. Alıntı bağlamda BİREBİR geçmeli, ≤150 karakter, tek satır.\n{baglam}")
    onb = ara / f"{alan}-{bolum[3]}.md"  # bölüm önbelleği: yeniden koşuda geçerli bölüm tekrar üretilmez
    if onb.is_file(): return onb.read_text(encoding="utf-8")
    for tur in ("orta", "zor", "orta"):
        y, k, log = ucretsiz_havuz.cagir(tur, istem, max_tokens=3000)
        iyi = suz(y) if y else []; (ara / "son-yanit.txt").write_text(y or "", encoding="utf-8")
        print(f"  {bolum[:30]} <- {k} · geçerli madde {len(iyi)}")
        if len(iyi) >= 3:
            onb.write_text(bolum + "\n" + "\n\n".join(iyi), encoding="utf-8"); return onb.read_text(encoding="utf-8")
    return None

parcalar = []
for b in re.findall(r"^## [A-E]\..+$", istem0, re.M):
    y = yaz(b)
    if y is None: sys.exit(5)
    parcalar.append(y)
A.write_text(f"# DERS KİTABI — {a['ad']}\n" + "\n\n".join(parcalar) + "\n", encoding="utf-8")
B_istem = f"ÇELİŞKİ DENETİMİ: aşağıdaki A taslağındaki her maddeyi kaynaklarla karşılaştır. Çıktı: madde başına `OK` / `ÇELİŞKİ: <neden>` / `DOĞRULANAMADI`; en sonda tek satır `SONUC: GECER` veya `SONUC: KALDI`.\n\n<A>\n{A.read_text(encoding='utf-8')}\n</A>\n{baglam}"
y = None
for tur in ("hakem", "zor", "orta"):
    y, k, log = ucretsiz_havuz.cagir(tur, B_istem, max_tokens=2500)
    if y: break
if not y: print("B çağrısı başarısız", log[-2:]); sys.exit(5)
B.write_text(y, encoding="utf-8")

alintilar = ALINTI.findall(A.read_text(encoding="utf-8"))
kotu = [q for q, d in alintilar if d not in bag or norm(q) not in bag[d]]
bsonuc = "SONUC: GECER" in B.read_text(encoding="utf-8")
print(f"alıntı {len(alintilar)} · birebir tutmayan {len(kotu)} · B {'GECER' if bsonuc else 'KALDI'}")
ok = alintilar and not kotu and bsonuc
hedef = (KASA / "30-okul" / alan) if ok else (ara / f"{alan}-TASLAK")
hedef.mkdir(parents=True, exist_ok=True)
(hedef / "ders-kitabi.md").write_bytes(A.read_bytes())
if ok:
    (KOK / f"docs/okul/{alan}.md").write_bytes(A.read_bytes())
    bg = KOK / "docs/okul/baglanti.json"
    d = json.loads(bg.read_text(encoding="utf-8")) if bg.exists() else {}
    d[alan] = {"ders": f"docs/okul/{alan}.md", "obsidian": f"30-okul/{alan}/ders-kitabi.md", "skill": a["anahtar"][:3]}
    bg.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("YAZILDI" if ok else f"TASLAK (girmedi): {hedef}"); sys.exit(0 if ok else 3)
