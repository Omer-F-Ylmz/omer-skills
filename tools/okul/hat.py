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
istem = (Path(__file__).with_name("sablon.md").read_text(encoding="utf-8")).format(ad=a["ad"], proje=a["proje"])
A, B = ara / f"{alan}-A.md", ara / f"{alan}-B.md"
print(f"{alan}: {len(kaynak)} kaynak"); 
if kuru: print("kuru: model çağrılmadı"); sys.exit(0)

def ucuz(soru, cikti, dosyalar):
    r = subprocess.run([sys.executable, str(KOK / "tools/ucuz_alt.py"), "--tur", "ozet", soru, str(cikti), *map(str, dosyalar)], capture_output=True, text=True, encoding="utf-8", errors="replace", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    print(r.stdout.strip()[-200:]); return r.returncode

rc = ucuz(istem, A, kaynak)
if rc not in (0, 3): sys.exit(rc)
if not re.search(r'^> "', A.read_text(encoding='utf-8'), re.M):
    print('A taslağında alıntı yok -> B atlandı, TASLAK'); sys.exit(3)
# B: bağımsız ikinci geçiş (zincir farklı model seçebilir; önbellek anahtarı istemle ayrışır)
rc = ucuz("ÇELİŞKİ DENETİMİ: A taslağındaki her maddeyi kaynaklarla karşılaştır. Çıktı: her madde için `OK` ya da `ÇELİŞKİ: <neden>` ya da `DOĞRULANAMADI`; en sonda tek satır `SONUC: GECER` veya `SONUC: KALDI`.", B, [A, *kaynak])
if rc not in (0, 3): sys.exit(rc)

metin = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in kaynak)
norm = lambda s: re.sub(r"\s+", " ", s).strip().lower()
havuz = norm(metin)
alintilar = re.findall(r'^> "(.+?)"', A.read_text(encoding="utf-8"), re.M)
kotu = [q for q in alintilar if norm(q) not in havuz]
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
