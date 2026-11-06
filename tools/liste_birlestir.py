"""LISTE-CIKAR-1 adım 2-3: det.jsonl + llm.jsonl -> tekilleştir, durum eşle -> docs/video-tarama/ana-liste.tsv + ana-liste-ozet.md"""
import csv, json, re, sys, collections
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
C = K / ".kos/kopru/ogren/liste-cikar-1"
OK = K / ".kos/kopru/ogren/video-izle-kur-1"
HOME = Path.home()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


csv.field_size_limit(10**9)


def tsv(p, kol=None):
    with open(p, encoding="utf-8", errors="replace", newline="") as f:
        return [r for r in csv.reader(f, delimiter="\t") if r]


# --- indeksler: norm ad -> (kaynak, durum)
calis, kurulu, kayit = {}, {}, {}
for r in tsv(OK / "tablo13.tsv")[1:]:
    (calis if re.search(r"calisiyor|kuruldu", r[3] if len(r) > 3 else "") else kurulu)[norm(r[0])] = ("tablo13.tsv", r[3] if len(r) > 3 else "")
for r in tsv(OK / "envanter.tsv")[1:]:
    if len(r) > 6:
        (calis if re.search(r"calisiyor|çalışıyor|kuruldu", r[6]) else kurulu)[norm(r[0])] = ("ogren/video-izle-kur-1/envanter.tsv", r[6])
for r in tsv(K / "docs/envanter/envanter.tsv")[1:]:
    kurulu.setdefault(norm(r[0]), ("docs/envanter/envanter.tsv", r[1] if len(r) > 1 else ""))
for d in (HOME / ".claude/skills").iterdir():
    kurulu.setdefault(norm(d.name), ("~/.claude/skills", d.name))
for d in (HOME / ".claude/plugins/cache").iterdir():
    kurulu.setdefault(norm(d.name), ("~/.claude/plugins/cache", d.name))
for p in sorted(OK.glob("kur-tur*.tsv")):  # iki sütun biçimi: ad,durum,... ve ad,repo,durum,...
    for r in tsv(p):
        d = next((c for c in r[1:3] if re.match(r"calisiyor|kuruldu", c.strip().lower())), "")
        if d and len(norm(r[0].lstrip("﻿"))) >= 3:
            calis.setdefault(norm(r[0].lstrip("﻿")), ("ogren/video-izle-kur-1/" + p.name, d))
KT = OK / "kurulu-tara.json"  # tools/kurulu_tara.py: PATH, pip, uv tool, npm -g, plugin cache, MCP
for a, src in (json.loads(KT.read_text(encoding="utf-8")).items() if KT.exists() else []):
    if len(norm(a)) >= 3:
        kurulu.setdefault(norm(a), ("kurulu-tara.json " + src, a))
for r in tsv(K / ".kos/kopru/kaynak-dizin/dizin.tsv")[1:]:
    kayit.setdefault(norm(r[1]) if len(r) > 1 else "", ("kaynak-dizin/dizin.tsv", r[0]))
calis_o = {re.sub(r"[^a-z0-9]", "", k.replace("0", "o").replace("rn", "m").replace("1", "l")): v for k, v in calis.items()}
kurulu_o = {re.sub(r"[^a-z0-9]", "", k.replace("0", "o").replace("rn", "m").replace("1", "l")): v for k, v in kurulu.items()}
usta = set()
for p in (K / "docs/usta").glob("*") if (K / "docs/usta").exists() else []:
    usta.add(norm(p.stem))
kart = {norm(p.stem) for p in (K / "docs/arac-kart").glob("*.md")} if (K / "docs/arac-kart").exists() else set()
kayit_jsonl = {norm(json.loads(l).get("ad", "")) for l in (K / "docs/kurulumlar/kayit.jsonl").read_text(encoding="utf-8").splitlines() if l.startswith("{")}

# --- kalemler
kal = {}  # anahtar -> dict
RDP = C / "repo-dogrula.json"
RD = json.loads(RDP.read_text(encoding="utf-8")) if RDP.exists() else {}
yok404 = set()
tablo = {norm(r[0]): r[3] for r in tsv(OK / "tablo13.tsv")[1:] if len(r) > 3}


def ocr(s):
    return norm(s).replace("0", "o").replace("rn", "m").replace("1", "l")


GENEL = re.compile(r"(agenttoolkit|toolkit|mcpserver|server|mcp|cli|skills?|plugin|sdk|js|py)$")


GENEL_AD = {"core", "cli", "app", "sdk", "server", "main", "docs", "skills", "plugin", "plugins", "web", "api", "mcp", "tools", "agent", "agents", "code"}


def kok(s):
    while (t := GENEL.sub("", s, count=1)) != s and len(t) >= 4:
        s = t
    return s


def lev1(a, b):  # Levenshtein <= 1 mi
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) > len(b):
        a, b = b, a
    i = j = 0
    fark = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1; j += 1
        else:
            fark += 1
            if fark > 1:
                return False
            if len(a) == len(b):
                i += 1
            j += 1
    return fark + (len(b) - j) + (len(a) - i) <= 1


def ekle(ad, tur, link, vid):
    ad = (ad or "").strip()
    if len(ad) < 2:
        return
    repo = ""
    m = re.search(r"github\.com/([\w.-]+/[\w.-]+)", link or "")
    if m:
        repo = m.group(1).removesuffix(".git")
        v = RD.get(repo) or {}
        if v.get("durum") == 404:
            if v.get("yakin"):
                link, repo = "https://github.com/" + v["yakin"], v["yakin"]
            else:
                yok404.add(repo.lower())
        elif v.get("tam"):
            repo = v["tam"]
        repo = repo.lower()
    key = repo or norm(ad)
    if not key:
        return
    e = kal.setdefault(key, {"ad": ad, "tur": collections.Counter(), "link": "", "vid": set()})
    e["tur"][tur or "arac"] += 1
    e["link"] = e["link"] or (link or "")
    e["vid"].add(vid)
    if repo:
        e["ad"] = e["ad"] if len(e["ad"]) >= len(repo.split("/")[1]) else repo.split("/")[1]


llm_ids, det_ids = set(), set()
BASLIK, TRU = {}, {}
for l in [x for fn in ("llm.jsonl", "llm-b.jsonl", "llm-c.jsonl", "llm-d2b.jsonl") if (C / fn).exists() for x in (C / fn).read_text(encoding="utf-8").splitlines() if x.strip()]:
    j = json.loads(l)
    llm_ids.add(j["id"])
    for k in j["kalemler"]:
        ekle(k.get("ad"), k.get("tur"), k.get("link"), j["id"])
for l in (C / "det.jsonl").read_text(encoding="utf-8").splitlines():
    j = json.loads(l)
    det_ids.add(j["id"])
    BASLIK[j["id"]], TRU[j["id"]] = j.get("baslik"), j.get("tr_uzun")
    for rp in j["repos"]:
        ekle(rp.split("/")[1], "arac", "https://github.com/" + rp, j["id"])

def birles(hedef, kaynak):
    h, k = kal[hedef], kal.pop(kaynak)
    h["tur"].update(k["tur"]); h["vid"] |= k["vid"]; h["link"] = h["link"] or k["link"]


# bulanık tekilleştirme: OCR ikizleri (0/o, rn/m, 1/l) ve tek harf farkı (ad >= 8 harf); repo anahtarı kazanır
rep = {ocr(k.split("/")[1]): k for k in kal if "/" in k}
for k in [k for k in kal if "/" not in k]:
    if ocr(k) in rep and rep[ocr(k)] in kal:
        birles(rep[ocr(k)], k)
duz = sorted((k for k in kal if "/" not in k), key=lambda x: (len(x), x))
kovalar = collections.defaultdict(list)
for k in duz:
    if k not in kal:
        continue
    o = ocr(k)
    hedef = next((d for d in kovalar[(o[:3], )] if d in kal and (ocr(d) == o or (len(o) >= 8 and lev1(ocr(d), o)))), None)
    if hedef:
        birles(hedef, k)
    else:
        kovalar[(o[:3], )].append(k)
sys.path.insert(0, str(K / "tools"))
from repo_dogrula import lev  # noqa: E402
gruplar = []  # çözülemeyen 404'ler: OCR bozuk varyantlar tek kalemde (en çok videoda geçen anahtar kalır)
for k in sorted((k for k in yok404 if k in kal), key=lambda x: -len(kal[x]["vid"])):
    h = next((g for g in gruplar if g in kal and lev(ocr(g), ocr(k)) <= max(3, len(k) // 7)), None)
    if h:
        birles(h, k); yok404.discard(k)
    else:
        gruplar.append(k)

TURLER = {"arac", "site-ucretsiz", "site-ilham", "ui-kutuphane", "prompt", "varlik", "kutuphane", "yontem"}
SITE = {"site-ucretsiz", "site-ilham"}
satirlar, say = [], collections.Counter()
for key, e in kal.items():
    tur = e["tur"].most_common(1)[0][0]
    tur = tur if tur in TURLER else "arac"
    n = norm(e["ad"])
    ana = norm(key.split("/")[1]) if "/" in key else n
    yer = ""
    t13 = tablo.get(n) or tablo.get(ana) or ""
    n, ana = ocr(n), ocr(ana)
    # genel ek/önek atılmış kök de denenir: "Gemini CLI" -> gemini, "Stripe Agent Toolkit" -> stripe
    aday = [x for x in dict.fromkeys([n, ana, kok(n), kok(ana)]) if len(x) >= 3 and x not in GENEL_AD]
    c_calis = next((calis_o[x] for x in aday if x in calis_o), None)
    c_kurulu = next((kurulu_o[x] for x in aday if x in kurulu_o and not (e["ad"][:1] in "./" and kurulu_o[x][0].startswith("kurulu-tara"))), None)
    if key in yok404:
        d, yer = "BULUNAMADI-ARANIYOR", "gh api repos/ 404; gh search yakın ad yok"
    elif c_calis:
        d, (src, kn) = "CALISIYOR", c_calis
        yer = src
    elif c_kurulu:
        d, (src, kn) = "KURULU-KANITSIZ", c_kurulu
        yer = src
    elif t13.startswith("hesap"):
        d, yer = "KURULMADI-HESAP", "tablo13.tsv"
    elif t13 == "bulunamadi":
        d, yer = "BULUNAMADI-ARANIYOR", "tablo13.tsv"
    elif tur in SITE | {"ui-kutuphane", "varlik", "kutuphane"}:
        if n in kayit:
            d, yer = "KAYITLI", kayit[n][0]
        else:
            d, yer = "KAYITSIZ", ""
    elif tur in ("prompt", "yontem"):
        d, yer = ("KAYITLI", "kayit.jsonl") if n in kayit_jsonl else ("KAYITSIZ", "")
    else:
        d = "KURULMADI-SIRADA"
    kanit = {"BULUNAMADI-ARANIYOR": "repo bulunamadı (404) / tablo13 bulunamadı", "KURULMADI-HESAP": "tablo13: hesap/anahtar gerekiyor",
             "CALISIYOR": "kurulum kaydı durumu", "KURULU-KANITSIZ": "envanter/skills/plugins dizininde var; gerçek çağrı kanıtı yok",
             "KAYITLI": "dizinde var", "KAYITSIZ": "dizinde yok", "KURULMADI-SIRADA": "hiçbir kurulu envanterde eşleşme yok"}[d]
    usta_var = "var" if (n in kart or n in usta or n in kayit_jsonl) else "yok"
    say[(tur, d)] += 1
    satirlar.append([e["ad"], tur, e["link"], ",".join(sorted(e["vid"]))[:400], d, kanit, usta_var, yer])

# kapı 3: aynı normalize ad -> tek satır (farklı repo anahtarları ' | ' ile birleşir, en iyi durum kalır)
ONCE = ["CALISIYOR", "KURULU-KANITSIZ", "KAYITLI", "KURULMADI-HESAP", "KURULMADI-SIRADA", "KAYITSIZ", "BULUNAMADI-ARANIYOR"]
grup = {}
for r in satirlar:
    g = grup.get(norm(r[0]))
    if g is None:
        grup[norm(r[0])] = list(r)
        continue
    g[3] = ",".join(sorted(set(g[3].split(",")) | set(r[3].split(","))))[:400]
    g[2] = " | ".join(dict.fromkeys(x for x in (g[2], r[2]) if x))
    if ONCE.index(r[4]) < ONCE.index(g[4]):
        g[4], g[5], g[7] = r[4], r[5], r[7]
    g[6] = "var" if "var" in (g[6], r[6]) else "yok"
    g[7] = g[7] or r[7]
satirlar = list(grup.values())
say = collections.Counter((r[1], r[4]) for r in satirlar)
satirlar.sort(key=lambda r: (r[1], r[0].lower()))
out = K / "docs/video-tarama/ana-liste.tsv"
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["kalem", "tur", "repo_link", "kaynak_video_idleri", "durum", "neden_kanit", "usta_karti", "bizde_nerede"])
    w.writerows(satirlar)

tum = len(det_ids)
bos = sorted(det_ids - llm_ids)
vsay = collections.Counter(d for _, d in say.elements()) if False else None
durum_say = collections.Counter()
for (t, d), c in say.items():
    durum_say[d] += c
tur_say = collections.Counter()
for (t, d), c in say.items():
    tur_say[t] += c
md = [f"# ANA-LISTE özeti (LISTE-CIKAR-1)\n",
      f"- İzlenen (tekil) video: {tum} (derin + derin-2)",
      f"- LLM ile işlenen: {len(llm_ids)} · işlenmeyen: {len(bos)}",
      f"- Çıkarılan tekil kalem: {len(satirlar)}", "", "## Tür başına", ""]
md += [f"- {t}: {c}" for t, c in sorted(tur_say.items())]
md += ["", "## Durum başına", ""] + [f"- {d}: {c}" for d, c in sorted(durum_say.items())]
md += ["", "## Tür × durum", ""] + [f"- {t} / {d}: {c}" for (t, d), c in sorted(say.items())]
bagli = set().union(*(e["vid"] for e in kal.values())) if kal else set()
icerik_yok = sorted(llm_ids - bagli)
md += ["", "## Kapsama ve kendi kendine kontrol", "",
       f"- video toplam {tum} = kalemi olan {len(bagli & det_ids)} + içerik-yok (LLM boş/kalem yok) {len(icerik_yok)} + LLM'den geçmemiş {len(bos)} · toplam kontrol: {len(bagli & det_ids) + len(icerik_yok) + len(bos)}",
       f"- kalem toplamı {len(satirlar)} = durumların toplamı {sum(durum_say.values())}",
       f"- repo doğrulama: {len(RD)} repo kontrol edildi, 200: {sum(1 for v in RD.values() if v.get('durum') == 200)}, 404: {sum(1 for v in RD.values() if v.get('durum') == 404)} (yakın ad bulunan: {sum(1 for v in RD.values() if v.get('yakin'))}), hata: {sum(1 for v in RD.values() if v.get('durum') == 'hata')}"]
(K / "docs/video-tarama/ana-liste-icerik-yok.txt").write_text("\n".join(f"{v}\t{BASLIK.get(v)}\tkonusma_karakter={TRU.get(v)}\tgerekce=LLM halkalari (haiku/pool) kalem donmedi; metinde arac/site adi yok" for v in icerik_yok) + "\n", encoding="utf-8")
md += ["", "## Sınırlar", "- RET / KURULMADI-HESAP / BULUNAMADI-ARANIYOR / SILINMIS-VIDEO bu turda atanmadı (kanıt gerektirir); KURULMADI-SIRADA = envanterde eşleşme yok, kurulum turu doğrular.",
       "- İşlenmeyen video id'leri: docs/video-tarama/ana-liste-islenmeyen.txt"]
(K / "docs/video-tarama/ana-liste-ozet.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(K / "docs/video-tarama/ana-liste-islenmeyen.txt").write_text("\n".join(bos) + "\n", encoding="utf-8")
print("\n".join(md))
