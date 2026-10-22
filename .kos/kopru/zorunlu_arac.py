"""ZORUNLU-ARAÇ-1 (Ömer 22 Eki): öğrenilen araçları görevde ZORUNLU kılar. ajan_sira.py kullanır.
blok(ad, metin): ön uçuş → araclar() (ZORUNLU-ARAÇ-2: anılan araçlar + tür çekirdeği + MCP profili + BM25 dolgu, ≤8 skill/ajan/cli/mcp) + `beyin ara` 3 ders + ruflo hata-dersi → isteme "ZORUNLU ARAÇLAR" bloğu; liste <ad>.zorunlu.json.
denetle(ad): bitişte oturum dökümü (session_id → ~/.claude/projects/*/<sid>.jsonl) sayılır; listeden ≥min(3, yarısı) araç kullanılmadıysa arac_eksik,
görsel iş türünde gorsel_hakem çağrısı yoksa kanit_eksik → <ad>.denetim.json (sonuc_kisa üst satırda gösterir).
  python zorunlu_arac.py --geri 10     son 10 görevi dökümden geriye dönük denetler (tablo)"""
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
SIRA = KOK / ".kos/kopru/ajan-sira"
GOREV = KOK / ".kos/kopru/gorev"
PROJELER = Path.home() / ".claude/projects"
N = 8
GORSEL = re.compile(r"(?i)site-3d|\b(3d|render\w*|video\w*|logo\w*|blender|webgl)\b")
NO_WIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def _calistir(argv, sure):
    try:
        r = subprocess.run(argv, cwd=KOK, capture_output=True, timeout=sure, creationflags=NO_WIN)
        return r.stdout.decode("utf-8", "replace").strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


YENIDEN = True  # arac_eksik → eksik araç ekiyle bir kez yeniden kuyruk (Ömer 22 Eki: bekleme yok)
GENEL = {"git", "mcp-server-git", "filesystem", "fetch", "memory", "time", "sequential-thinking"}
CEKIRDEK = [  # (tür, desen, sabit çekirdek set); en çok eşleşen tür kazanır, eşitlikte tür yok
    ("site-3d", r"(?i)site-3d|sketchfab|objaverse|gltf|\bglb\b|\b(site|landing|three(\.js)?|webgl|3d|frontend)\b",
     ["threejs-3d-paket", "gsap-skills:gsap-core", "web-sahne-desenleri", "frontend-craft"]),
    ("render", r"(?i)\b(render\w*|blender)\b", ["blender-uretim"]),
    ("video", r"(?i)\bvideo\w*", ["video-tarama", "video-uygula", "remotion-video-paket", "hyperframes-paket"]),
    ("kurulum", r"(?i)\b(kurulum\w*|install\w*)", ["awesome-rehber", "gitleaks", "semgrep"]),
]
try:  # ZORUNLU-ARAÇ-3 katman 2: tools/tur_setleri.json'daki yeni türler (mevcut 4 tür aynen kalır)
    TUR_SET = json.loads((KOK / "tools/tur_setleri.json").read_text(encoding="utf-8"))
except (OSError, ValueError):
    TUR_SET = {"cekirdek": {}, "desen": {}, "turler": {}}
for _t, _d in TUR_SET["desen"].items():
    if _t not in {c[0] for c in CEKIRDEK} and _t in TUR_SET["turler"]:
        CEKIRDEK.append((_t, _d, TUR_SET["turler"][_t]["skill"] + TUR_SET["turler"][_t]["cli"]))
CEKIRDEK_AD = {a for _, _, c in CEKIRDEK for a in c} | {a.split(":")[-1] for _, _, c in CEKIRDEK for a in c}
AYARLAR = Path.home() / ".claude/settings.json"
GECMIS = KOK / ".kos/kopru/kombin-gecmis.jsonl"
CANLI_TUR = {"site-3d", "kod-backend"}  # canlı/yayın deseni yalnız bu türlerde tam seti ekler
KOD_TUR = {"site-3d", "kod-backend", "guvenlik", "mod", "kurulum", "render"}  # graphify çekirdeği yalnız kod işinde zorunlu


def kapsam(metin):
    """Başlık (önekli 'ad-N —' atılmış) + İLK VE BAĞLAYICI bölümü; bölüm yoksa ilk 800 karakter."""
    satir = metin.lstrip().split("\n", 1)
    baslik = re.sub(r"^#+\s*([\w-]+\s*[—-]\s*)?", "", satir[0])
    m = re.search(r"(?s)## İLK VE BAĞLAYICI\s*(.*?)(?=\n## |\Z)", metin)
    return baslik + "\n" + (m.group(1)[:1500] if m else (satir[1] if len(satir) > 1 else "")[:800])


def tur_bul(kap):
    """(tür adı, çekirdek set) — eşitlikte ya da eşleşme yoksa ('diğer', [])."""
    say = sorted(((len(re.findall(d, kap)), t, c) for t, d, c in CEKIRDEK), key=lambda x: -x[0])
    if say[0][0] == 0 or say[0][0] == say[1][0]:
        return "diğer", []
    return say[0][1], say[0][2]


def canli_set(kap):
    """Canlıya çıkacak/kullanıcıya açık iş: tasarım+görsel+içerik+SEO+a11y+güvenlik+test+KVKK+yayın tam seti; desen yoksa []."""
    c = TUR_SET.get("canli")
    return c["skill"] + c["cli"] if c and re.search(c["desen"], kap) else []


def sablon_araclari(kap):
    """İş türü şablonu (site/uygulama/video/araç/otomasyon): en çok eşleşen, ≥2 eşleşmeli → varsayılan araç kombini."""
    say = sorted(((len(re.findall(s["desen"], kap)), s["araclar"]) for s in TUR_SET.get("sablon", {}).values()), key=lambda x: -x[0])
    return say[0][1] if say and say[0][0] >= 2 and (len(say) < 2 or say[0][0] > say[1][0]) else []


def yaratici(metin, tur):
    """Tür için yaratıcı araç kombini önerisi (REA + Playwright SS + context7 ...); tür yoksa 'diğer' satırı."""
    y = TUR_SET.get("yaratici", {})
    return y.get(tur) or y.get("diğer", "")


def _kayit(o):
    return {"ad": o["ad"], "tur": o["tur"], "cagri": o["cagri"], "ne": (o["is"] or o["metin"])[:90]}


def araclar(metin):
    """ZORUNLU-ARAÇ-2, ≤N kayıt: görevde adı geçen araçlar (≤4) → tür çekirdek seti → MCP profili (mcp_profil) → BM25 (başlık+tür, eşik) dolgusu.
    Sorgu görev metninin tamamı değil kapsam() (başlık + İLK VE BAĞLAYICI); git/mcp-server-git gibi genel kayıtlar elenir."""
    sys.path.insert(0, str(KOK / "tools"))
    try:
        import katalog_ara
        import mcp_profil
        rows = [json.loads(s) for s in katalog_ara.KATALOG.read_text(encoding="utf8").splitlines()]
    except Exception:
        return []
    kap = kapsam(metin)
    tur, cek = tur_bul(kap)
    sira = {"skill": 0, "ajan": 1, "cli": 2}  # ad → kayıt; aynı ad/kısa adda skill önde, mcp/plugin denetlenemez
    dizin = {}
    for o in sorted((o for o in rows if o["tur"] in sira or o["tur"] == "arac"), key=lambda o: (sira.get(o["tur"], 3), ":" in o["ad"])):
        if o["ad"] not in GENEL and "reposunda" not in o["metin"]:
            dizin.setdefault(o["ad"], o)
            dizin.setdefault(o["ad"].split(":")[-1], o)
    sec, goruldu = [], set()

    sinir = [N]  # N tavanı yalnız BM25 dolgusuna; tür çekirdeği ve anılan araçlar tavansız

    def ekle(o, tavan=True):
        k = o["ad"].split(":")[-1]
        if k not in goruldu and (not tavan or len(sec) < sinir[0]):
            goruldu.add(k)
            sec.append(_kayit(o))

    kod = set(re.findall(r"`([^`\s]+)`", kap))
    anilan = {}
    for t in re.findall(r"[\w][\w:.-]*", kap):
        t = t.rstrip(".:-")
        if t in dizin and len(t) >= 5 and (re.search(r"[-_:]", t) or t in kod or t in CEKIRDEK_AD) and t not in anilan:
            anilan[t] = kap.count(t)
    for t in sorted(anilan, key=lambda t: -anilan[t])[:4]:
        ekle(dizin[t], False)
    for a in cek:
        if a in dizin:
            ekle(dizin[a], False)
    for a in sablon_araclari(kap) + (canli_set(kap) if tur in CANLI_TUR else []):
        if a in dizin:
            ekle(dizin[a], False)
    sinir[0] = max(N, len(sec) + 3)
    tanim = mcp_profil.tanimlar()
    for m in mcp_profil.sec(metin):  # ajan_sira --mcp-config ile aynı girdi/profil: oturumda gerçekten yüklenenler
        if tur != "diğer" and m not in mcp_profil.TEMEL and m in tanim and len([o for o in sec if o["tur"] == "mcp"]) < 2:
            if m not in goruldu:
                goruldu.add(m)
                sec.append({"ad": m, "tur": "mcp", "cagri": f"mcp__{m}__*", "ne": "MCP profilinde (görev türü)"})
    q = f"{kap.splitlines()[0]} {tur if tur != 'diğer' else ''}"
    puan, gerek = katalog_ara.puanla(q, satirlar=rows)
    tepe = puan[0][0] if puan else 0
    bm = [o for s, kap_, o in puan[:40] if s >= 0.6 * tepe and kap_ >= gerek and o["tur"] in sira and o["ad"] not in GENEL
          and "reposunda" not in o["metin"]]
    if tur != "diğer" and len(bm) < 3:  # tür biliniyorsa kapı en az 3 BM25 aracı döndürür (eşik gevşer)
        bm += [o for _, _, o in puan[:40] if o not in bm and o["tur"] in sira and o["ad"] not in GENEL and "reposunda" not in o["metin"]][:3 - len(bm)]
    for o in katalog_ara.suz(bm, katalog_ara.yigin(q))[0]:
        ekle(o)
    return sec


RUFLO_KOD = """import sys, os, json
sys.path.insert(0, 'C:/Projeler/omer-skills/tools/ruflo')
os.environ['CLAUDE_FLOW_MCP_TOOLS'] = 'agentdb_pattern-search'
import mcp_dene
o, _ = mcp_dene.kos([('tools/call', {'name': 'agentdb_pattern-search', 'arguments': {'query': sys.argv[1], 'topK': 3}})])
r = json.loads(o[max(o)]['result']['content'][0]['text']).get('results')
print(json.dumps(r, ensure_ascii=False) if r else '')
"""



def ruflo_ders(metin):
    """agentdb_pattern-search (hata-dersi); MCP açılamazsa ya da sonuç boşsa ''."""
    return _calistir([sys.executable, "-I", "-c", RUFLO_KOD, "hata-dersi " + metin[:300]], 45)[:700]


def kombinler(metin, k=2):
    """ZORUNLU-ARAÇ-3 katman 3: tür kombinlerinden en iyi k → [{id, adimlar: [araç adları]}]; hata/tür yoksa []."""
    try:
        sys.path.insert(0, str(KOK / "tools"))
        import kombin_sec
        kap = kapsam(metin)
        tur = tur_bul(kap)[0]
        if tur == "diğer":
            return []
        ks = kombin_sec.sec(kap, k, tur)[1]
        return [{"id": o["id"], "adimlar": [a for a, _ in o["adimlar"]]} for o in ks]
    except Exception:
        return []


def blok(ad, metin):
    ar = araclar(metin)
    if not ar:
        return ""
    ders = _calistir([sys.executable, "-I", str(KOK / "tools/beyin.py"), "ara", metin[:300], "--k", "3", "--butce", "450"], 40)
    hata = ruflo_ders(metin)
    kombin = kombinler(metin)
    tur = tur_bul(kapsam(metin))[0]
    gec = gecmis_ders(tur)
    (SIRA / f"{ad}.zorunlu.json").write_text(json.dumps({"araclar": ar, "gorsel": bool(GORSEL.search(metin)), "kombin": kombin,
                                                         "tur": tur, "hata": hata[:200],
                                                         "onucus": [a for a, v in (("beyin", ders), ("ruflo", hata)) if v]}, ensure_ascii=False), encoding="utf-8")
    s = ["ZORUNLU ARAÇLAR (bitişte oturum dökümünden sayılır; ≥%d kullanılmazsa görev arac_eksik işaretlenir ve yeniden kuyruğa girer):" % min(3, math.ceil(len(ar) / 2))]
    s += [f"- {o['ad']} ({o['tur']}) · {o['ne']} · çağrı: {o['cagri'][:60]}" for o in ar]
    s.append("PLAN TABLOSU: her araç için ilk turda tek satır `araç | kullanılacak adım / kullanılmama gerekçesi`; gerekçesiz atlama = arac_eksik.")
    if GORSEL.search(metin):
        s.append("- gorsel_hakem (görsel iş: `python .kos/kopru/gorsel_hakem.py` çağrısı olmadan kanit_eksik)")
    s += [f"- KOMBİN {o['id']}: " + " > ".join(o["adimlar"]) for o in kombin]
    s.append("YARATICI KOMBİN: " + yaratici(metin, tur))
    if gec:
        s.append(f"GEÇMİŞ ({tur}): {gec}")
    s.append("ÇEKİRDEK (her iş, tam): beyin · ruflo · claude-mem · rtk · headroom · context-mode · graphify(kod). "
             "ÖĞRENME: başta ruflo pattern-search+beyin ara; sonda beyin kaydet+ruflo pattern-store+hooks_intelligence_learn")
    if ders:
        s.append("Beyin dersleri:\n" + ders[:900])
    if hata:
        s.append("Hata-dersi (ruflo): " + hata)
    return "\n".join(s) + "\n\n"


def gecmis_yaz(ad, tur, liste, den):
    """Kombin kütüphanesi: iş türü → araç listesi → eksik → durum (ön uçuş bundan öğrenir); en iyi çaba."""
    try:
        with GECMIS.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ad": ad, "tur": tur, "araclar": [o["ad"] for o in liste], "eksik": den.get("eksik", []),
                                "durum": den["durum"], "t": int(time.time())}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def gecmis_ders(tur, k=3):
    """Aynı türün geçmişinden: en çok atlanan araçlar (eksik/iş) + temiz biten son işler; kayıt yoksa ''."""
    try:
        satirlar = [json.loads(s) for s in GECMIS.read_text(encoding="utf-8").splitlines() if s.strip()]
    except (OSError, ValueError):
        return ""
    ayni = [r for r in satirlar if r.get("tur") == tur]
    if not ayni:
        return ""
    atlanan = {}
    for r in ayni:
        for a in r.get("eksik", []):
            atlanan[a] = atlanan.get(a, 0) + 1
    s = "en çok atlanan: " + ", ".join(f"{a} {n}/{len(ayni)}" for a, n in sorted(atlanan.items(), key=lambda x: -x[1])[:k])
    iyi = [r["ad"] for r in ayni if r.get("durum") == "ok"][-2:]
    return s + (" · temiz biten: " + ", ".join(iyi) if iyi else "")


def ajan_adlari(ad):
    """blok()'un yazdığı <ad>.zorunlu.json'daki ajan adları; dosya yok/bozuk → ()."""
    try:
        return tuple(o["ad"] for o in json.loads((SIRA / f"{ad}.zorunlu.json").read_text(encoding="utf-8"))["araclar"] if o["tur"] == "ajan")
    except (OSError, ValueError, KeyError):
        return ()


def _kullanimlar(sid):
    """Döküm → (Skill adları, Agent tipleri, mcp araç adları, Bash komutları); döküm yoksa None."""
    yol = next(iter(PROJELER.glob(f"*/{sid}.jsonl")), None)
    if not yol:
        return None
    sk, ag, mcp, sh = [], [], [], []
    for l in yol.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            m = json.loads(l).get("message") or {}
        except ValueError:
            continue
        for b in m.get("content") if isinstance(m.get("content"), list) else ():
            if b.get("type") != "tool_use":
                continue
            ad, gir = b.get("name", ""), b.get("input") or {}
            if ad == "Skill":
                sk.append(str(gir.get("skill", "")))
            elif ad in ("Agent", "Task"):
                ag.append(str(gir.get("subagent_type", "")))
            elif ad.startswith("mcp__"):
                mcp.append(ad)
            elif ad == "Bash":
                sh.append(str(gir.get("command", "")))
    return sk, ag, mcp, sh


def _kullanildi(o, k):
    sk, ag, mcp, sh = k
    ad = o["ad"]
    if o["tur"] in ("skill", "plugin"):
        return any(s.split(":")[-1] == ad.split(":")[-1] for s in sk)  # katalog adı ad-alanlı olabilir (frontend-craft:frontend-craft)
    if o["tur"] == "ajan":
        return ad in ag
    sozcuk = re.compile(r"(?i)(?<![\w-])" + re.escape(ad) + r"(?![\w-])")
    return any(sozcuk.search(c) for c in sh) or any(f"mcp__{ad}__" in m for m in mcp)


def karar(liste, gorsel, k):
    """(durum, kullanılmayanlar) — saf karar; k = _kullanimlar çıktısı."""
    yok = [o["ad"] for o in liste if not _kullanildi(o, k)]
    durum = []
    if liste and len(yok) >= min(3, math.ceil(len(liste) / 2)):
        durum.append("arac_eksik")
    if gorsel and not any("gorsel_hakem" in c for c in k[3]):
        durum.append("kanit_eksik")
    return "+".join(durum) or "ok", yok


def _ad_kullanildi(ad, k):
    """Kombin adımı/çekirdek adı: Skill, Agent, Bash komutu ya da mcp araç adında geçiyor mu."""
    sk, ag, mcp, sh = k
    kisa = ad.split(":")[-1].split("/")[-1]
    sozcuk = re.compile(r"(?i)(?<![\w-])" + re.escape(kisa) + r"(?![\w-])")
    return (any(s.split(":")[-1] == kisa for s in sk) or kisa in ag or any(sozcuk.search(c) for c in sh)
            or any(kisa.replace("-", "_") in m.replace("-", "_") for m in mcp))


CEKIRDEK_KULLAN = {  # ZORUNLU-ARAÇ-3 katman 1: ad → (skill/ajan/Bash/mcp adı olarak aranan eşanlamlılar)
    "beyin": ("beyin",), "ruflo": ("ruflo", "claude-flow", "agentdb"), "claude-mem": ("claude-mem",), "rtk": ("rtk",),
    "headroom": ("headroom", "headroom-compress"), "context-mode": ("context-mode", "strategic-compact", "context-mode-paket"),
    "graphify": ("graphify", "sor2"),
}
OGRENME_BASTA = ("pattern-search", "beyin.py ara", "beyin ara")
OGRENME_SONDA = ("pattern-store", "beyin.py kaydet", "beyin kaydet", "hooks_intelligence_learn")


def pasif_var(a):
    """rtk/headroom/claude-mem/context-mode hook·vekil·eklenti olarak çalışır, dökümde tool_use bırakmaz → ayarlarda kayıtlıysa kullanılmış sayılır."""
    try:
        return a in TUR_SET.get("pasif", []) and a in AYARLAR.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def cekirdek_ogrenme(tur, k, onucus=()):
    """(çekirdekte kullanılmayanlar, öğrenme döngüsü eksikleri) — katman 1 / 1b; graphify yalnız KOD_TUR'da zorunlu.
    onucus: blok()'un ön uçuşta gerçekten sorgulayıp isteme koyduğu çekirdek araçlar (beyin ara, ruflo pattern-search) → kullanılmış ve 'basta' tamam."""
    yok = [a for a, es in CEKIRDEK_KULLAN.items() if (a != "graphify" or tur in KOD_TUR) and not pasif_var(a) and a not in onucus and not any(_ad_kullanildi(e, k) for e in es)]
    metin = " ".join(k[3] + k[2])
    ogr = [n for n, kel in (("basta", OGRENME_BASTA), ("sonda", OGRENME_SONDA)) if not (n == "basta" and onucus) and not any(x in metin for x in kel)]
    return yok, ogr


def tekrar_hata(ad, hata):
    """Aynı hata-dersi, daha önce *_eksik ile biten bir görevde de önümüze geldiyse True (katman 1b-d) — öneri dosyasına satır düşer."""
    if not hata:
        return False
    for p in SIRA.glob("*.zorunlu.json"):
        if p.name == f"{ad}.zorunlu.json":
            continue
        try:
            if json.loads(p.read_text(encoding="utf-8")).get("hata") != hata:
                continue
            if "eksik" in json.loads((SIRA / p.name.replace(".zorunlu", ".denetim")).read_text(encoding="utf-8")).get("durum", ""):
                with (KOK / ".kos/kopru/on-soz-oneri.md").open("a", encoding="utf-8") as f:
                    f.write(f"- {ad}: aynı hata-dersi {p.name.split('.')[0]} görevinde de eksik bitti → on-söz kuralı öner: {hata[:120]}\n")
                return True
        except (OSError, ValueError):
            continue
    return False


def denetle(ad):
    """<ad>.json + <ad>.zorunlu.json → <ad>.denetim.json ({durum, eksik, kombin, cekirdek, ogrenme}); liste ya da döküm yoksa None."""
    try:
        z = json.loads((SIRA / f"{ad}.zorunlu.json").read_text(encoding="utf-8"))
        sid = json.loads((SIRA / f"{ad}.json").read_text(encoding="utf-8")).get("session_id")
    except (OSError, ValueError):
        return None
    k = _kullanimlar(sid) if sid else None
    if k is None:
        return None
    d = _hesapla(ad, z, k)
    (SIRA / f"{ad}.denetim.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    if "tur" in z:
        gecmis_yaz(ad, z["tur"], z["araclar"], d)
    return d


def _hesapla(ad, z, k, yan=True):
    """Saf denetim kararı (yan=False: tekrar_hata dosya yazmaz)."""
    durum, yok = karar(z["araclar"], z["gorsel"], k)
    d = {"durum": durum, "eksik": yok}
    if "tur" in z:  # ZORUNLU-ARAÇ-3 alanları; eski (katman-3 öncesi) dosyalarda yok
        kul = [(o["id"], sum(_ad_kullanildi(a, k) for a in o["adimlar"]), len(o["adimlar"])) for o in z.get("kombin", [])]
        cek, ogr = cekirdek_ogrenme(z["tur"], k, z.get("onucus", ()))
        d.update(kombin=[f"{i} {n}/{t}" for i, n, t in kul], cekirdek_eksik=cek, ogrenme_eksik=ogr)
        d["durum"] = "+".join(x for x in [durum if durum != "ok" else "", "arac_eksik" * bool(cek and "arac_eksik" not in durum),
                                          "ogrenme_eksik" * bool(ogr), "tekrar_hata" * (yan and tekrar_hata(ad, z.get("hata", "")))] if x) or "ok"
    return d


def oran_yeniden(adlar):
    """(arac_eksik sayısı, toplam): kayıtlı liste+döküm bugünkü kararla yeniden hesaplanır (önce/sonra ölçümü)."""
    say = eksik = 0
    for ad in adlar:
        try:
            z = json.loads((SIRA / f"{ad}.zorunlu.json").read_text(encoding="utf-8"))
            k = _kullanimlar(json.loads((SIRA / f"{ad}.json").read_text(encoding="utf-8")).get("session_id"))
        except (OSError, ValueError):
            continue
        if k is None:
            continue
        say += 1
        eksik += "arac_eksik" in _hesapla(ad, z, k, False)["durum"]
    return eksik, say


ISARET = ("arac_eksik", "kanit_eksik", "ogrenme_eksik")


def devam(ad, den):
    """(devam turu adı | None, durum): üç işaretten biri varsa eksik → x-a, x-a2; ikinci devamdan sonra hâlâ eksikse (None, 'dur'); işaret yoksa (None, 'ok')."""
    if not any(i in den["durum"] for i in ISARET):
        return None, "ok"
    if ad.endswith("-a2"):
        return None, "dur"
    return (ad[:-2] + "-a2" if ad.endswith("-a") else ad + "-a"), "devam"


def eksik_liste(den):
    """Denetim sonucundan devam turunda koşulacak eksiklerin sıralı listesi."""
    e = list(den.get("eksik", [])) + list(den.get("cekirdek_eksik", []))
    if "kanit_eksik" in den["durum"]:
        e.append("gorsel_hakem")
    return e + ["öğrenme:" + x for x in den.get("ogrenme_eksik", [])]


def yeniden_istem(ad, istem, eksik, yeni=None):
    """Eksik araçlarla yeniden kuyruk için görev dosyası (KOK'a göreli yol döner)."""
    yol = GOREV / f"{yeni or ad + '-a'}.md"
    yol.write_text((KOK / istem).read_text(encoding="utf-8") + f"\n\nÖnceki tur işi yaptı; baştan yapma, yalnız eksik adımı koş. kullanmadığın araçlar: {', '.join(eksik)} — bu turda bunları kullan.\n", encoding="utf-8")
    return str(yol.relative_to(KOK)).replace("\\", "/")


def kosul_uyari(kosul, istem):
    """tsv koşul alt dizesi görev dosyasının kendi içinde geçiyorsa uyarı metni, yoksa ''."""
    if not kosul or "::" not in kosul:
        return ""
    yol, alt = kosul.split("::", 1)
    try:
        if alt in (KOK / istem).read_text(encoding="utf-8"):
            return f"koşul alt dizesi görev dosyasının kendi içinde geçiyor ({alt!r}) → görev hemen başlar"
    except OSError:
        pass
    return ""


def geri(n):
    """Son n görev: tsv'den istem → blok listesi (bugünkü katalogla) → mevcut dökümle karar. Tablo yazdırır."""
    tsv = {s.split("\t")[0]: s.split("\t")[1] for s in (KOK / ".kos/kopru/ajan-sira.tsv").read_text(encoding="utf-8").splitlines()
           if "\t" in s and not s.startswith("#")}
    adaylar = sorted((p for p in SIRA.glob("*.json") if p.stem in tsv and p.stat().st_size > 0), key=lambda p: p.stat().st_mtime)
    say = eksik = 0
    print("ad\tliste\tkullanılan\tdurum\ttür\taday")
    for p in reversed(adaylar):
        if say == n:
            break
        try:
            sid = json.loads(p.read_text(encoding="utf-8")).get("session_id")
            metin = (KOK / tsv[p.stem]).read_text(encoding="utf-8")
        except (OSError, ValueError):
            continue
        k = _kullanimlar(sid) if sid else None
        ar = araclar(metin)
        if k is None or not ar:
            continue
        durum, yok = karar(ar, bool(GORSEL.search(metin)), k)
        say += 1
        eksik += durum != "ok"
        print(f"{p.stem}\t{len(ar)}\t{len(ar) - len(yok)}\t{durum}\t{tur_bul(kapsam(metin))[0]}\t{' '.join(o['ad'] for o in ar)}")
    print(f"toplam {say} · işaretlenen {eksik}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 2 and sys.argv[1] == "--geri":
        geri(int(sys.argv[2]))
    elif len(sys.argv) > 2 and sys.argv[1] == "--oran":
        _d = sorted(SIRA.glob("*.denetim.json"), key=lambda p: p.stat().st_mtime)[-int(sys.argv[2]):]
        _once = sum("arac_eksik" in json.loads(p.read_text(encoding="utf-8")).get("durum", "") for p in _d)
        _son, _n = oran_yeniden([p.name.split(".")[0] for p in _d])
        print(f"son {len(_d)} denetim · kayıtlı arac_eksik {_once} · bugünkü kararla {_son}/{_n} (%{100 * _son // max(_n, 1)})")
    elif len(sys.argv) > 1:  # görev dosyası → tür + zorunlu araç listesi; boş liste hata
        _m = Path(sys.argv[1]) if Path(sys.argv[1]).is_absolute() else KOK / sys.argv[1]
        _m = _m if _m.exists() else GOREV / _m.name
        _t = _m.read_text(encoding="utf-8")
        _a = araclar(_t)
        print(f"tür: {tur_bul(kapsam(_t))[0]} · {len(_a)} araç")
        for _o in _a:
            print(f"- {_o['ad']} ({_o['tur']}) · {_o['ne']}")
        sys.exit(0 if _a else 1)
