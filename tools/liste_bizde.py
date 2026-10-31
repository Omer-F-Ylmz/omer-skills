"""LISTE-CIKAR-1 adım 6 (NİHAİ 36): ana-liste.tsv her kalemi için 'bizde nerede' — birleşik dizin + kurulu skill/plugin/klon/uygulama/envanter kaynakları.
Eşleşme: normalize ad eşitliği (repo biçiminde repo adı). Çıktı: bizde_nerede sütunu (mevcut değer korunur, 'kategori:yol' eklenir) + ana-liste-ozet.md 'Taranan kaynaklar' bölümü.
Kullanım: python -I tools/liste_bizde.py"""
import collections
import csv
import re
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
L = K / "docs/video-tarama/ana-liste.tsv"
OZET = K / "docs/video-tarama/ana-liste-ozet.md"
HOME = Path.home()
csv.field_size_limit(10**7)


def n(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def anahtarlar(ad):
    ad = str(ad).strip()
    ks = {n(ad)}
    if "/" in ad:
        ks.add(n(ad.rstrip("/").split("/")[-1]))
    return {k for k in ks if len(k) >= 4}


IDX = collections.defaultdict(list)  # anahtar -> [(kategori, yol)]
SAY = collections.Counter()
KAYNAK = {}


def ekle(kat, yol, ad):
    for k in anahtarlar(ad):
        IDX[k].append((kat, yol))


def tsv(p, kat, adkol, yolkol=None, katkol=None):
    p = Path(p)
    if not p.exists():
        KAYNAK[kat + ":" + p.name] = "yok"
        return
    sat = 0
    with open(p, encoding="utf-8", errors="replace", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            sat += 1
            ad = r.get(adkol) or ""
            ekle(r.get(katkol) or kat if katkol else kat, str(p.relative_to(K)) if p.is_relative_to(K) else str(p), ad)
    KAYNAK[kat + ":" + p.name] = sat


# 1) birleşik kaynak dizini (tür başına kategori)
tsv(K / ".kos/kopru/kaynak-dizin/dizin.tsv", "dizin", "ad", katkol="tur")
# 2) kurulu katalog (skill/ajan/mcp/cli/sec/bizim)
tsv(K / "docs/katalog/yetenek.tsv", "katalog", "ad", katkol="kaynak")
# 3) kaynak-kutuphane + ek sınıf + envanterler
for p in ("docs/kaynak-kutuphane/envanter.tsv", "docs/kaynak-kutuphane/ek-kaynak-sinif.tsv", "docs/kaynak-kutuphane/site-katalog-tur4.tsv",
          "docs/kaynak-kutuphane/kutuphane-haritasi.tsv", "docs/envanter/envanter.tsv", "docs/envanter/arac-ajan-ozellik.tsv",
          ".kos/kopru/ogren/video-izle-kur-1/envanter.tsv", ".kos/kopru/ogren/video-izle-kur-1/tablo13.tsv",
          ".kos/kopru/ogren/video-izle-kur-1/kurulacaklar-temiz.tsv"):
    q = K / p
    if q.exists():
        with open(q, encoding="utf-8", errors="replace", newline="") as f:
            kol = csv.DictReader(f, delimiter="\t")
            ilk = kol.fieldnames[0]
            sat = 0
            for r in kol:
                sat += 1
                ekle("kaynak-kutuphane/envanter", p, r.get(ilk) or "")
        KAYNAK["envanter:" + q.name] = sat
# 4) kurulu skill / plugin / klon / MCP
sk = HOME / ".claude/skills"
if sk.exists():
    ds = [d.name for d in sk.iterdir()]
    for d in ds:
        ekle("kurulu-skill", "~/.claude/skills/" + d, d)
    KAYNAK["kurulu-skill:~/.claude/skills"] = len(ds)
for kok, kat in ((HOME / ".claude/plugins/marketplaces", "plugin-pazar"), (K / "araclar", "klon"), (Path(r"C:/AI/indirilen"), "indirilen"),
                 (HOME / "Desktop/Claude ile yapılanlar", "kendi-proje")):
    if kok.exists():
        ds = [d.name for d in kok.iterdir()]
        for d in ds:
            ekle(kat, str(kok).replace(str(HOME), "~") + "/" + d, d)
        KAYNAK[kat + ":" + kok.name] = len(ds)
# 5) bilgisayardaki uygulamalar
for p in (".kos/kopru/tmp/her_sey.txt", ".kos/kopru/tmp/kor_nokta.txt"):
    q = K / p
    if q.exists():
        ls = q.read_text(encoding="utf-8", errors="replace").splitlines()
        for l in ls:
            ekle("uygulama", p, re.split(r"\s{2,}|\t|\|", l.strip())[0])
        KAYNAK["uygulama:" + q.name] = len(ls)
# 6) kaynak-kütüphane site/klon alt dizinleri
for alt in ("site", "klon"):
    d = K / "docs/kaynak-kutuphane" / alt
    if d.exists():
        ds = [x.name for x in d.iterdir()]
        for x in ds:
            ekle("kaynak-kutuphane/" + alt, f"docs/kaynak-kutuphane/{alt}/{x}", Path(x).stem)
        KAYNAK[f"kaynak-kutuphane/{alt}:dizin"] = len(ds)

rows = list(csv.DictReader(open(L, encoding="utf-8", newline=""), delimiter="\t"))
kat_say, eslesen = collections.Counter(), 0
for r in rows:
    bul = []
    for k in anahtarlar(r["kalem"]) | anahtarlar(r["repo_link"].split("|")[0].replace("https://github.com/", "")):
        for kat, yol in IDX.get(k, []):
            if (kat, yol) not in bul and yol != str(L.relative_to(K)):
                bul.append((kat, yol))
    mevcut = r["bizde_nerede"]
    ek = [f"{kat}:{yol}" for kat, yol in bul[:4] if f"{kat}:{yol}" not in mevcut and yol not in mevcut]
    if bul:
        eslesen += 1
        for kat in {b[0] for b in bul}:
            kat_say[kat] += 1
    r["bizde_nerede"] = "; ".join(x for x in ([mevcut] if mevcut else []) + ek)

with open(L, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)

dolu = sum(1 for r in rows if r["bizde_nerede"])
bol = ["", "## Taranan kaynaklar ve 'bizde nerede' eşleşmeleri (NİHAİ 36G)", "",
       f"- kalem {len(rows)} · bizde_nerede dolu {dolu} · bu taramada eşleşen {eslesen} (ad eşitliği, normalize)", "", "Kaynak (satır/öğe sayısı):", ""]
bol += [f"- {k} · {v}" for k, v in sorted(KAYNAK.items())]
bol += ["", "Kategori başına eşleşen kalem:", ""] + [f"- {k} · {v}" for k, v in kat_say.most_common()]
t = OZET.read_text(encoding="utf-8")
t = t.split("\n## Taranan kaynaklar")[0].rstrip("\n")
OZET.write_text(t + "\n" + "\n".join(bol) + "\n", encoding="utf-8")
print("kalem", len(rows), "dolu", dolu, "eslesen", eslesen, dict(kat_say.most_common(8)))
