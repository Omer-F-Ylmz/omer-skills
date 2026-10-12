"""RUFLO-1 A/B: 3 aile (kod · rapor · video) × 5 ardışık görev × derssiz/dersli = 30 sonnet koşusu + dersli kolda 15 haiku
damıtması = 45 claude -p (tavan 60), Σ$ kesici 9.5. Her görev klasöründe KURALLAR.md var, istemde anılmaz: gizli ölçüt
(belgelenmemiş proje kuralı). Derssiz kol keşifle bulabilir; dersli kol önceki koşuların yargıç notlarından damıtılan
dersle (ReasoningBank: yörünge → yargıç → damıtma → birleştirme → geri çağırma). Kollar görev görev sırayla koşar.
  python ab_olc.py --kuru   → çağrısız: yargıçların başlangıç < 1 ve örnek çözüm = 1 verdiğini doğrular
  python ab_olc.py          → ölçüm; satırlar docs/kutuphane/olcum/ruflo-1-ab.tsv, banka .kos/ogrenme-ab/<zaman>/"""
import csv
import io
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KOK / "tools" / "olcum"), str(KOK / "tools" / "ogrenme")]
import ders  # noqa: E402
import onsoz  # noqa: E402

TSV = KOK / "docs" / "kutuphane" / "olcum" / "ruflo-1-ab.tsv"
CAGRI_TAVAN, USD_TAVAN = 60, 9.5
EK = ["--permission-mode", "acceptEdits", "--allowedTools", "Read,Edit,Write,Glob,Grep,Bash(python:*)",
      "--strict-mcp-config", "--max-turns", "20"]

# --- kod: harf duyarsız işlemler; gizli kural Türkçe I/İ ---
KOD_KURAL = "# Proje kuralları\n- Harf duyarsız karşılaştırma/sayma/sıralama her yerde `yardimci.tr_kucuk` ile yapılır (str.lower/casefold Türkçe I/İ'yi bozar).\n"
YARDIMCI = 'def tr_kucuk(s):\n    return s.replace("I", "ı").replace("İ", "i").lower()\n'
KOD = [  # (ad, hatalı gövde, doğru gövde, görünür testler, gizli testler)
    ("say", "def say(metin, kelime):\n    return metin.split().count(kelime)\n",
     "def say(metin, kelime):\n    return [tr_kucuk(w) for w in metin.split()].count(tr_kucuk(kelime))\n",
     ['say("Elma elma ELMA armut", "elma") == 3'], ['say("IRMAK ırmak Irmak", "ırmak") == 3']),
    ("benzersiz", "def benzersiz(kelimeler):\n    return list(set(kelimeler))\n",
     "def benzersiz(kelimeler):\n    g, o = set(), []\n    for k in kelimeler:\n        if tr_kucuk(k) not in g:\n            g.add(tr_kucuk(k))\n            o.append(k)\n    return o\n",
     ['benzersiz(["Elma", "elma", "Armut"]) == ["Elma", "Armut"]'], ['benzersiz(["İzmir", "izmir", "Iğdır", "ığdır"]) == ["İzmir", "Iğdır"]']),
    ("basla_mi", "def basla_mi(metin, onek):\n    return onek.lower().startswith(metin.lower())\n",
     "def basla_mi(metin, onek):\n    return tr_kucuk(metin).startswith(tr_kucuk(onek))\n",
     ['basla_mi("Merhaba dünya", "merhaba") is True', 'basla_mi("Merhaba", "dünya") is False'], ['basla_mi("İSTANBUL", "ist") is True']),
    ("sirala", "def sirala(kelimeler):\n    return sorted(kelimeler, reverse=True)\n",
     "def sirala(kelimeler):\n    return sorted(kelimeler, key=tr_kucuk)\n",
     ['sirala(["b", "A", "c"]) == ["A", "b", "c"]'], ['sirala(["Işık", "ilaç", "İnek"]) == ["ilaç", "İnek", "Işık"]']),
    ("esit_mi", "def esit_mi(a, b):\n    return a.lower() == b.lower()\n",
     "def esit_mi(a, b):\n    return tr_kucuk(a.strip()) == tr_kucuk(b.strip())\n",
     ['esit_mi(" Elma", "elma ") is True'], ['esit_mi("KIRMIZI", "kırmızı") is True']),
]

# --- rapor: CSV özeti; gizli kural biçim ---
RAPOR_KURAL = "# Rapor kuralları\n- rapor.md ilk satırı tam olarak `# Özet`\n- En fazla 6 satır\n- Sayılar binlik ayırıcı nokta, ondalıksız: 12.345\n- Tarihler GG.AA.YYYY\n"
RAPOR = [("tutar", "son"), ("adet", "ilk"), ("tutar", "ilk"), ("adet", "son"), ("tutar", "son")]

# --- video: transkriptten araç etiketi; gizli kural şema ---
VIDEO_KURAL = '# Etiket kuralları\n- etiket.json: {"araclar": [...], "kaynak": "transkript.txt"}\n- Araç adları küçük harf, alfabetik sıralı, yinelenmesiz\n- Yalnız kurulabilir yazılım araçları; şirket/kişi adı değil\n'
VIDEO = [
    ("Bu videoda Ruflo ile ajan sürüsü kurduk, Graphify ile kod grafiği çıkardık, kesimi FFmpeg ile yaptık. Anthropic ekibine teşekkürler.", ["ffmpeg", "graphify", "ruflo"]),
    ("Playwright ile testleri koştum, sonra Vite projesini Tailwind ile süsledim. Google'ın sunumu ilham verdi.", ["playwright", "tailwind", "vite"]),
    ("Whisper ile altyazı çıkardım, yt-dlp ile indirdim, Blender'da sahneyi kurdum. Teşekkürler OpenAI.", ["blender", "whisper", "yt-dlp"]),
    ("Remotion ile video kodladık, Three.js ile 3B sahne, GSAP ile animasyon. Microsoft'un etkinliğinde gösterdik.", ["gsap", "remotion", "three.js"]),
    ("SkillSpector ile skill'leri taradım, uv ile Python ortamı kurdum, Ollama ile yerel model koştum. Meta'nın modeli kullanıldı.", ["ollama", "skillspector", "uv"]),
]


def _satis(i):
    r = random.Random(i)
    return [(f"2026-{r.randint(1, 9):02d}-{r.randint(1, 28):02d}", r.choice(["çay", "kahve", "fincan"]), r.randint(50, 400), r.randint(500, 5000)) for _ in range(12)]


def _tr_sayi(n):
    return f"{n:,}".replace(",", ".")


def kur(aile, i, d):
    """Görev klasörünü kurar → istem."""
    d = Path(d)
    if aile == "kod":
        ad, hatali = KOD[i][0], KOD[i][1]
        (d / "KURALLAR.md").write_text(KOD_KURAL, encoding="utf-8")
        (d / "yardimci.py").write_text(YARDIMCI, encoding="utf-8")
        (d / "islev.py").write_text("from yardimci import tr_kucuk  # noqa: F401\n\n\n" + hatali, encoding="utf-8")
        (d / "test_islev.py").write_text("from islev import *  # noqa\n\n\ndef test_gorunur():\n" + "".join(f"    assert {t}\n" for t in KOD[i][3]), encoding="utf-8")
        return f"islev.py içindeki `{ad}` fonksiyonu hatalı (harf duyarsız çalışmalı). Düzelt; test_islev.py geçmeli."
    if aile == "rapor":
        (d / "KURALLAR.md").write_text(RAPOR_KURAL, encoding="utf-8")
        b = io.StringIO()
        csv.writer(b, lineterminator="\n").writerows([("tarih", "urun", "adet", "tutar"), *_satis(i)])
        (d / "satis.csv").write_text(b.getvalue(), encoding="utf-8")
        olcu, tarih = RAPOR[i]
        return f"satis.csv'deki toplam {olcu} ile en {'son' if tarih == 'son' else 'eski'} satış tarihini kısa bir rapor olarak rapor.md'ye yaz."
    (d / "KURALLAR.md").write_text(VIDEO_KURAL, encoding="utf-8")
    (d / "transkript.txt").write_text(VIDEO[i][0], encoding="utf-8")
    return "transkript.txt'de anılan yazılım araçlarını etiket.json'a JSON olarak yaz."


def coz(aile, i, d):
    """Örnek doğru çözüm (yalnız --kuru yargıç sınaması)."""
    d = Path(d)
    if aile == "kod":
        (d / "islev.py").write_text("from yardimci import tr_kucuk\n\n\n" + KOD[i][2], encoding="utf-8")
    elif aile == "rapor":
        n, t = _beklenen_rapor(i)
        (d / "rapor.md").write_text(f"# Özet\n- Toplam: {_tr_sayi(n)}\n- Tarih: {t[8:]}.{t[5:7]}.{t[:4]}\n", encoding="utf-8")
    else:
        (d / "etiket.json").write_text(json.dumps({"araclar": VIDEO[i][1], "kaynak": "transkript.txt"}), encoding="utf-8")


def _beklenen_rapor(i):
    s, (olcu, tarih) = _satis(i), RAPOR[i]
    return sum(x[2 if olcu == "adet" else 3] for x in s), (max if tarih == "son" else min)(x[0] for x in s)


def yargic(aile, i, d):
    """→ (puan 0..1, gizli kısım 0..0.5, notlar). Görünür ölçüt 0.5, gizli (KURALLAR.md) 0.5."""
    d, notlar = Path(d), []
    if aile == "kod":
        gor, giz = KOD[i][3], KOD[i][4]  # eval yalnız bu dosyadaki sabit test ifadeleri, ayrı süreçte
        betik = "import json, islev\nfrom islev import *\nr = []\nfor t in %r:\n    try:\n        r.append(bool(eval(t)))\n    except Exception:\n        r.append(False)\nprint(json.dumps(r))\n" % (gor + giz)
        try:
            r = json.loads(subprocess.run([sys.executable, "-c", betik], cwd=d, capture_output=True, text=True, timeout=30).stdout.strip().splitlines()[-1])
        except Exception:
            r = [False] * (len(gor) + len(giz))
        notlar += [f"{'görünür' if k < len(gor) else 'gizli'} test başarısız: {t}" for k, (t, ok) in enumerate(zip(gor + giz, r)) if not ok]
        a, b = sum(r[:len(gor)]) / len(gor) * 0.5, sum(r[len(gor):]) / len(giz) * 0.5
        return round(a + b, 3), round(b, 3), notlar
    if aile == "rapor":
        f = d / "rapor.md"
        metin = f.read_text(encoding="utf-8") if f.exists() else ""
        n, t = _beklenen_rapor(i)
        g, tr = "", f"{t[8:]}.{t[5:7]}.{t[:4]}"
        a = 0.25 * (str(n) in re.sub(r"[.,\s]", "", metin)) + 0.25 * any(x in metin for x in (t, tr, tr.replace(".", "/")))
        satir = [s for s in metin.strip().splitlines()]
        kont = [(satir[:1] == ["# Özet"], "ilk satır tam olarak '# Özet' değil"), (0 < len(satir) <= 6, "6 satırdan uzun"),
                (_tr_sayi(n) in metin, f"sayı binlik ayırıcı noktayla yazılmadı (ör. {_tr_sayi(n)})"), (tr in metin, "tarih GG.AA.YYYY değil")]
        notlar += [("eksik: " if a < 0.5 else "") + "görünür ölçüt (doğru sayı/tarih)"] if a < 0.5 else []
        notlar += [f"gizli ölçüt: {m}" for ok, m in kont if not ok]
        b = 0.125 * sum(ok for ok, _ in kont)
        return round(a + b, 3), round(b, 3), notlar
    f, bek = d / "etiket.json", VIDEO[i][1]
    try:
        j = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return 0.0, 0.0, ["etiket.json yok ya da JSON değil"]
    liste = next((v for v in (j.values() if isinstance(j, dict) else [j]) if isinstance(v, list)), [])
    norm = lambda s: re.sub(r"[^a-z0-9ığüşöç]", "", str(s).lower())  # noqa: E731
    k1, k2 = {norm(x) for x in liste}, {norm(x) for x in bek}
    a = 0.5 * len(k1 & k2) / len(k1 | k2) if k1 | k2 else 0
    ar = j.get("araclar") if isinstance(j, dict) else None
    kont = [(isinstance(ar, list), "anahtar 'araclar' değil"),
            (isinstance(ar, list) and ar == sorted(set(ar)) and all(str(x) == str(x).lower() for x in ar), "araç adları küçük harf + alfabetik + yinelenmesiz değil"),
            (isinstance(j, dict) and j.get("kaynak") == "transkript.txt", "'kaynak': 'transkript.txt' alanı yok")]
    if a < 0.5:
        notlar.append(f"görünür ölçüt: araç kümesi eksik/fazla (Jaccard {a * 2:.2f})")
    notlar += [f"gizli ölçüt: {m}" for ok, m in kont if not ok]
    b = 0.5 * sum(ok for ok, _ in kont) / len(kont)
    return round(a + b, 3), round(b, 3), notlar


AJAN = {"kod": "ab-kod", "rapor": "ab-rapor", "video": "ab-video"}
DAMIT = ("Bir ajan koşusunun yargıç sonucu aşağıda. Gelecekteki BENZER görevlerde işe yarayacak en fazla 3 genellenebilir ders çıkar "
         "(kural/yöntem; bu göreve özgü sayı ya da dosya içeriği değil). Puan < 1 ise her yargıç notu için bir düzeltici ders "
         "(hatanın kaynağı + ilk turda ne yapılmalı). Dersler tur sayısını da azaltmalı: ek doğrulama turu önerme, bağımsız okumaları "
         "aynı turda paralel yap, yazma ve kontrolü tek adımda birleştir. icerik tek cümle (≤20 kelime), örneksiz. "
         # d8: video/rapor'da dersli kolun ek 2-3 turu gizli kural belgesini bulup okumaktı → kural derse gömülür, belge yeniden okunmaz
         "Proje kural belgesi bu görev ailesinde sabittir: kurallarını TEK derste somut yaz (anahtar adları, biçim, sıra; tek cümle, "
         "≤30 kelime, noktalı virgülle) ki sonraki görev belgeyi okumadan uygulasın. "
         "Yalnız JSON liste döndür, başka metin yok: "
         '[{"baslik": "kural", "kosul": "ne zaman uygulanır", "icerik": "ne yapılmalı"}]\n'
         "Görev: %s\nPuan: %s/1 (ölçütler görev klasörünün belgelerinden)\nTur: %s\nYargıç notları: %s\nAjanın son mesajı: %s\n"
         "Görev klasöründeki proje kural belgesi (yörüngede okunabilir): %s")


def kuru():
    for aile, n in (("kod", 5), ("rapor", 5), ("video", 5)):
        for i in range(n):
            with tempfile.TemporaryDirectory() as d:
                kur(aile, i, d)
                bas = yargic(aile, i, d)
                coz(aile, i, d)
                son = yargic(aile, i, d)
                assert bas[0] < 1 and son == (1.0, 0.5, []), (aile, i, bas, son)
    print("kuru: 15 görev · yargıç başlangıç < 1, örnek çözüm = 1")


def v2(tohum, aile, ad="v2"):
    """d5: getir ≤2 ders/≤120 jeton + görev metniyle eşleşme + yeni damıtma. Taban = ab.tsv derssiz satırları (görevler deterministik);
    yalnız dersli kol, görev 2..5. d6: aile başına ayrı süreç/banka/TSV (paralel); tohum yalnız v1'in 1. görev dersleri (sonraki
    görevlerin dersleri aynı görevi önceden görmek olurdu), gerisini v2 kendi damıtır.
    d7 (v3): v1 → v2 arasında sistem istemi ~+15k cache_creation büyüdü (20:28 KALİTE-3 yayılımı) → v1 derssiz taban geçersiz;
    v3 derssiz kolu aynı süreçte, aynı anda koşar."""
    # v4: d7 tur talimatıyla yalnız dersli kol; taban = v3 derssiz satırları (~20 dk önce, aynı sistem istemi — cache_creation ile denetle)
    kollar, tavan = {"v3": (("derssiz", "dersli"), (12, 3.6)), "v4": (("dersli",), (8, 1.45))}.get(ad, (("dersli",), (8, 2.5)))
    banka = KOK / ".kos" / "ogrenme-ab" / (f"{ad}-{aile}-" + time.strftime("%Y%m%d-%H%M%S"))
    os.environ["OGRENME_DIZIN"] = str(banka)
    for x in (json.loads(s) for s in (Path(tohum) / "dersler.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()):
        m = re.match(r"ab-(kod|rapor|video)(\d)", x["kaynaklar"][0])
        if x["durum"] == "aktif" and m and m[1] == aile and m[2] == "0":
            with tempfile.TemporaryDirectory() as d:
                ders.ekle(x["ajan"], x["baslik"], x["kosul"], x["icerik"], x["tur"], x["kaynaklar"][0], x["kanit"], kur(m[1], int(m[2]), d))
    print(time.strftime("%H:%M:%S"), f"{ad} tohum: {len(ders.oku())} ders ({banka})", flush=True)
    main((banka, 0, 0), aileler=(aile,), siralar=range(1, 5), kollar=kollar, tsv=TSV.with_name(f"ruflo-1-ab-{ad}-{aile}.tsv"),
         tavan=tavan)


def main(devam=None, aileler=("kod", "rapor", "video"), siralar=range(5), kollar=("derssiz", "dersli"), tsv=TSV,
         tavan=(CAGRI_TAVAN, USD_TAVAN)):
    """devam = (banka, çağrı, usd): yarım koşuyu aynı bankayla sürdürür; TSV'deki (aile, sıra, kol) atlanır, tavanlar toplamda."""
    import kosucu
    TSV, (CAGRI_TAVAN, USD_TAVAN) = tsv, tavan  # noqa: N806
    banka = Path(devam[0]) if devam else KOK / ".kos" / "ogrenme-ab" / time.strftime("%Y%m%d-%H%M%S")
    banka.mkdir(parents=True, exist_ok=bool(devam))
    os.environ["OGRENME_DIZIN"] = str(banka)
    yeni = not TSV.exists()
    cagri, usd = (int(devam[1]), float(devam[2])) if devam else (0, 0.0)
    bitti = set() if yeni else {tuple(x.split("	")[1:4]) for x in TSV.read_text(encoding="utf-8").splitlines()[1:]}
    with open(TSV, "a", encoding="utf-8", newline="\n") as out:
        if yeni:
            out.write("zaman\taile\tsira\tkol\tpuan\tgizli\ttur\tinput\tcache_creation\tcache_read\toutput\tusd\tsure_sn\tders_ids\trc\tnotlar\n")
        for aile in aileler:
            for i in siralar:
                for kol in kollar:
                    if (aile, str(i + 1), kol) in bitti:
                        continue
                    if cagri + (2 if kol == "dersli" else 1) > CAGRI_TAVAN or usd >= USD_TAVAN or kosucu.bos_ram_gb() < 1.6:  # Ömer 13 Eki: RAM %95'e kadar (31.7 GB × %5)
                        print(time.strftime("%H:%M:%S"), f"TAVAN: {cagri} çağrı ${usd:.2f} boş RAM {kosucu.bos_ram_gb():.1f} GB — durdu", flush=True)
                        return
                    d = tempfile.mkdtemp(prefix=f"ruflo-ab-{aile}{i}-")
                    gorev = kur(aile, i, d)
                    istem, ids = onsoz.istem(AJAN[aile], gorev) if kol == "dersli" else (gorev, [])
                    o = kosucu.kos(istem, ek=EK, cwd=d, model="sonnet", butce=0.6)
                    cagri, usd = cagri + 1, usd + o["usd"]
                    puan, gizli, notlar = yargic(aile, i, d)
                    if kol == "dersli":
                        ders.geri_bildir(ids, puan >= 1.0) if ids else None
                    if kol == "dersli" and i < max(siralar):  # son görevin dersi bu ölçümde kullanılmaz → damıtma çağrısı yok
                        dm = kosucu.kos(DAMIT % (gorev, puan, o["tur"], "; ".join(notlar) or "hepsi geçti", o["metin"][-1500:],
                                                 (Path(d) / "KURALLAR.md").read_text(encoding="utf-8")),
                                        ek=["--strict-mcp-config", "--max-turns", "1"], model="haiku", butce=0.2)
                        cagri, usd = cagri + 1, usd + dm["usd"]
                        try:
                            m = dm["metin"]
                            for x in json.loads(m[m.index("["):m.rindex("]") + 1])[:3]:
                                ders.ekle(AJAN[aile], x["baslik"], x["kosul"], x["icerik"], "basari" if puan >= 1.0 else "basarisizlik",
                                          f"ab-{aile}{i}", f"puan {puan}", gorev)
                        except (ValueError, KeyError, TypeError) as e:
                            print(time.strftime("%H:%M:%S"), f"damıtma ayrışmadı {aile}{i}: {e}", flush=True)
                    u = kosucu.jeton(o["usage"])
                    out.write("\t".join(map(str, [time.strftime("%H:%M:%S"), aile, i + 1, kol, puan, gizli, o["tur"], *u, round(o["usd"], 4),
                                                  o["sure"], ",".join(ids), o["rc"], " | ".join(notlar)[:300]])) + "\n")
                    out.flush()
                    print(time.strftime("%H:%M:%S"), aile, i + 1, kol, "puan", puan, "tur", o["tur"], f"${o['usd']:.3f}", "dersler", ids, f"Σ{cagri} ${usd:.2f}", flush=True)
    print(time.strftime("%H:%M:%S"), f"BİTTİ: {cagri} çağrı ${usd:.2f} · banka {banka}", flush=True)


if __name__ == "__main__":
    if "--kuru" in sys.argv:
        kuru()
    elif "--v5" in sys.argv:  # d8: kural derse gömülü; boş bankayla eşli (derssiz+dersli), aile başına ≤14 çağrı/$4
        aile = sys.argv[sys.argv.index("--v5") + 1]
        main((KOK / ".kos" / "ogrenme-ab" / f"v5-{aile}-{time.strftime('%Y%m%d-%H%M%S')}", 0, 0), aileler=(aile,),
             tsv=TSV.with_name(f"ruflo-1-ab-v5-{aile}.tsv"), tavan=(14, 4.0))
    elif {"--v2", "--v3", "--v4"} & set(sys.argv):
        ad = next(a for a in ("v4", "v3", "v2") if "--" + a in sys.argv)
        v2(*sys.argv[sys.argv.index("--" + ad) + 1:][:2], ad=ad)
    else:
        main(sys.argv[sys.argv.index("--devam") + 1:][:3] if "--devam" in sys.argv else None)
