"""ZORUNLU-ARAÇ-1 (Ömer 22 Eki): öğrenilen araçları görevde ZORUNLU kılar. ajan_sira.py kullanır.
blok(ad, metin): ön uçuş → araclar() (ZORUNLU-ARAÇ-2: anılan araçlar + tür çekirdeği + MCP profili + BM25 dolgu, ≤8 skill/ajan/cli/mcp) + `beyin ara` 3 ders + ruflo hata-dersi → isteme "ZORUNLU ARAÇLAR" bloğu; liste <ad>.zorunlu.json.
denetle(ad): bitişte oturum dökümü (session_id → ~/.claude/projects/*/<sid>.jsonl) sayılır; listeden ≥min(3, yarısı) araç kullanılmadıysa arac_eksik,
görsel iş türünde gorsel_hakem çağrısı yoksa kanit_eksik → <ad>.denetim.json (sonuc_kisa üst satırda gösterir).
  python zorunlu_arac.py --geri 10     son 10 görevi dökümden geriye dönük denetler (tablo)"""
import json
import math
import re
import shutil
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


UI_ARAC = {"departman-frontend", "frontend-craft", "impeccable", "pixeljury", "playwright-cli", "scroll-craft", "web-sahne-desenleri",
           "threejs-3d-paket", "gsap-core", "seo-audit", "accessibility-audit", "copywriting", "marketing-skills", "fe-meta-seo-duzeltici",
           "lighthouse-chrome-devtools", "strix", "ecc-agentshield"}  # yalnız kullanıcıya açık web/UI çıktısında zorunlu
IC_ISARET = re.compile(r"(?i)\.py\b|\.kos/|\btools/|\bbetik\w*|\bajan_sira\b|\bders kitab\w*|\bmüfredat\w*|\bdokümantasyon\b|\bkart_dogrula\b")
UI_TESLIM = re.compile(r"(?i)\blanding\b|\bcanl[ıi]ya\b|\byayına\b|\barayüz\w*\s+(yap|tasarla|kur)|\bsite\s+(yap|kur|tasarla|üret)|\bpixeljury\b|\b3d site\b")


GUV_IC = ("semgrep", "gitleaks")  # NİHAİ-DÜZELT-2 (Desktop kararı 1): kod değiştiyse zorunlu
GUV_DIS = {"strix", "ecc-agentshield", "skillspector"}  # yalnız dış kod/bağımlılık/skill-plugin kurulumunda zorunlu
KOD_ISARET = re.compile(r"(?i)\.(py|mjs|js|ts|ps1)\b|\btools/|\bbetik\w*|\bkod\b|\bajan_sira\b")
DIS_KOD = re.compile(r"(?i)\bkurulum\w*|\binstall\w*|\bklon\w*|\bclone\w*|\bbağımlılık\w*|\bdependenc\w*|\bplugin\w*|\beklenti\w*|\bskill\s+(kur|yükle)\w*")
METIN_ISI = re.compile(r"(?i)\bders kitab\w*|\bmüfredat\w*|\bmetin\b|\bdokümantasyon\b|\.(tsv|csv|md|txt)\b|\bbirleştir\w*")
# DENETİM-AYAR-1: araç gereksinimi görev metnindeki anahtar sözcükten değil işin ÇIKTI türünden (teslim edilen dosya/eylem) türer
GORSEL_DOSYA = re.compile(r"(?i)\.(png|jpe?g|svg|webp|gif|glb|gltf|blend|mp4|mov|webm)\b")
VIDEO_ARAC = {"video-tarama", "video-uygula", "remotion-video-paket", "hyperframes-paket"}
VIDEO_CIKTI = re.compile(r"(?i)youtu(\.be|be\.com)|\.(mp4|mov|webm|mkv)\b|\bvideo\w*\s+(üret|render|kes|montaj|yap|kur|oluştur|düzenle)\w*|\b(üret|render|oluştur)\w*\s+video|\bremotion\b|\bhyperframes\b")
ARAMA_ARAC = {"awesome-rehber"}
ARAMA_CIKTI = re.compile(r"(?i)\bawesome\b|dış araç|araç\s+(ara|bul|keşf|öner)\w*|yeni araç|araç aday\w*")


def kod_guvenligi(kap):
    """(kod değişiyor mu, dış kod/bağımlılık/skill-plugin kurulumu var mı) — semgrep+gitleaks ilkine, strix/agentshield/skillspector ikincisine bağlı."""
    return bool(KOD_ISARET.search(kap)), bool(DIS_KOD.search(kap))


def gorsel_gerek(metin):
    """Desktop kararı 2: görsel-hakem yalnız görsel çıktı üreten işte; ders kitabı/metin işi (UI teslimi yoksa) görsel sayılmaz."""
    kap = kapsam(metin)
    return bool(GORSEL.search(metin)) and (not METIN_ISI.search(kap) or bool(UI_TESLIM.search(kap) or GORSEL_DOSYA.search(kap)))


def ui_isi(kap):
    """Çıktı kullanıcıya açık web/UI mi: iç-iş işareti var ve güçlü UI teslimi yoksa False (SEO/a11y/frontend/strix zorunlu olmaz)."""
    return not IC_ISARET.search(kap) or bool(UI_TESLIM.search(kap))


def gerekceli(ad, eksik):
    """Ajan raporunda 'atlandı/kullanılmadı + neden' satırı olan eksik araçlar (kısa ad, aynı satırda gerekçe işareti)."""
    try:
        r = json.loads((SIRA / f"{ad}.json").read_text(encoding="utf-8")).get("result") or ""
    except (OSError, ValueError):
        return []
    sat = [s for s in r.splitlines() if re.search(r"(?i)atlan|kullanılmad|kullanmad|gerek(siz| yok|mez)|uygun değil|kapsam dışı", s)]
    return [e for e in eksik if any(e.split(":")[-1].lower() in s.lower() and re.search(r"(?i)çünkü|neden|—|:|->|→|\(.{8,}\)", s) for s in sat)]


def gorsel_gerekceli(ad):
    """Ajan raporunda 'görsel çıktı yok/üretmedi' türü gerekçe satırı var mı."""
    try:
        r = json.loads((SIRA / f"{ad}.json").read_text(encoding="utf-8")).get("result") or ""
    except (OSError, ValueError):
        return False
    return any(re.search(r"(?i)g[öo]rsel", s) and re.search(r"(?i)yok|üretmedi|gerek(siz|mez)|atlan|kullanılmad|değil", s) for s in r.splitlines())


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


def erisim_yok(o):
    """AJAN-TAM-YETKI-1: düz adlı cli PATH'te yoksa True (npm paketi/skill/mcp denetlenmez)."""
    return o["tur"] == "cli" and bool(re.fullmatch(r"[\w.-]+", o["ad"])) and not shutil.which(o["ad"])


def _kayit(o, dolgu=False):
    k = {"ad": o["ad"], "tur": o["tur"], "cagri": o["cagri"], "ne": (o["is"] or o["metin"])[:90]}
    if dolgu:  # BM25/MCP dolgusu: önerilir, zorunlu sayılmaz (ilgisiz araç dayatma hatası, 23 Eki)
        k["dolgu"] = True
    return k


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
            sec.append(_kayit(o, tavan))

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
                sec.append({"ad": m, "tur": "mcp", "cagri": f"mcp__{m}__*", "ne": "MCP profilinde (görev türü)", "dolgu": True})
    q = f"{kap.splitlines()[0]} {tur if tur != 'diğer' else ''}"
    puan, gerek = katalog_ara.puanla(q, satirlar=rows)
    tepe = puan[0][0] if puan else 0
    bm = [o for s, kap_, o in puan[:40] if s >= 0.6 * tepe and kap_ >= gerek and o["tur"] in sira and o["ad"] not in GENEL
          and "reposunda" not in o["metin"]]
    if tur != "diğer" and len(bm) < 3:  # tür biliniyorsa kapı en az 3 BM25 aracı döndürür (eşik gevşer)
        bm += [o for _, _, o in puan[:40] if o not in bm and o["tur"] in sira and o["ad"] not in GENEL and "reposunda" not in o["metin"]][:3 - len(bm)]
    for o in katalog_ara.suz(bm, katalog_ara.yigin(q))[0]:
        ekle(o)
    if not ui_isi(kap):  # NİHAİ-DÜZELT-1: iç betik / ders kitabı işi SEO·a11y·frontend·strix dayatmaz (önerilir, zorunlu değil)
        for o in sec:
            if o["ad"].split(":")[-1] in UI_ARAC:
                o["dolgu"] = True
    kod_var, dis_var = kod_guvenligi(kap)  # NİHAİ-DÜZELT-2
    for o in sec:
        k = o["ad"].split(":")[-1]
        if (k in GUV_DIS and not dis_var) or (k in GUV_IC and not kod_var) or (  # DENETİM-AYAR-1: çıktı türü kapıları (adı görevde geçen araç hariç)
                k not in kap and ((k in VIDEO_ARAC and not VIDEO_CIKTI.search(kap)) or (k in ARAMA_ARAC and not ARAMA_CIKTI.search(kap)))):
            o["dolgu"] = True
    if kod_var:
        for a in GUV_IC:
            if a in dizin:
                ekle(dizin[a], False)
        for o in sec:
            if o["ad"].split(":")[-1] in GUV_IC:
                o.pop("dolgu", None)
    for o in sec:  # erişilemeyen araç zorunlu sayılmaz (denetime girmez), blok'ta "ERİŞİM YOK" satırı
        if erisim_yok(o):
            o["dolgu"] = o["yok"] = True
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


SECICI_KOK = None  # test: sahte kart kökü


def secici_satir(metin, tur):
    """BEYIN-ARAC-KART-1: işe özel önerilen küme (arac_ara.sec: kart sırası + geçmişte birlikte KABUL alan eşler + iş türü tarifi); kart yoksa ''."""
    try:
        sys.path.insert(0, str(KOK / "tools"))
        import arac_ara
        r = arac_ara.sec(kapsam(metin), SECICI_KOK, None if tur == "diğer" else tur)
        return "SEÇİCİ (arac_ara, işe özel, isteğe bağlı): " + ", ".join(r["kume"]) if r["kume"] else ""
    except Exception:
        return ""


def blok(ad, metin):
    ar = araclar(metin)
    if not ar:
        return ""
    ders = _calistir([sys.executable, "-I", str(KOK / "tools/beyin.py"), "ara", metin[:300], "--k", "3", "--butce", "450"], 40)
    hata = ruflo_ders(metin)
    kombin = kombinler(metin)
    tur = tur_bul(kapsam(metin))[0]
    gec = gecmis_ders(tur)
    (SIRA / f"{ad}.zorunlu.json").write_text(json.dumps({"araclar": ar, "gorsel": gorsel_gerek(metin), "kombin": kombin,
                                                         "tur": tur, "hata": hata[:200],
                                                         "onucus": [a for a, v in (("beyin", ders), ("ruflo", hata)) if v]}, ensure_ascii=False), encoding="utf-8")
    s = ["ZORUNLU ARAÇLAR (bitişte oturum dökümünden sayılır; ≥%d kullanılmazsa görev arac_eksik işaretlenir ve yeniden kuyruğa girer):" % min(3, math.ceil(len([o for o in ar if not o.get("dolgu")]) / 2))]
    s += [f"- {o['ad']} ({o['tur']}) · {o['ne']} · çağrı: {o['cagri'][:60]}" for o in ar if not o.get("dolgu")]
    if any(o.get("dolgu") and not o.get("yok") for o in ar):
        s.append("İSTEĞE BAĞLI (zorunlu değil, işe uyarsa kullan): " + ", ".join(o["ad"] for o in ar if o.get("dolgu") and not o.get("yok")))
    if any(o.get("yok") for o in ar):
        s.append("ERİŞİM YOK (bu makinede kurulu değil, zorunlu sayılmaz): " + ", ".join(o["ad"] for o in ar if o.get("yok")))
    s.append("PLAN TABLOSU: her araç için ilk turda tek satır `araç | kullanılacak adım / kullanılmama gerekçesi`; gerekçesiz atlama = arac_eksik.")
    if gorsel_gerek(metin):
        s.append("- gorsel_hakem (görsel iş: `python .kos/kopru/gorsel_hakem.py` çağrısı olmadan kanit_eksik)")
    s += [f"- KOMBİN {o['id']}: " + " > ".join(o["adimlar"]) for o in kombin]
    if sec := secici_satir(metin, tur):
        s.append(sec)
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


def _tarama_basarisiz():
    try:
        d = json.loads((KOK / ".kos/kopru/tarama-durum.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return any(isinstance(v, dict) and v.get("rc") == 3 for v in d.values())


def karar(liste, gorsel, k):
    """(durum, kullanılmayanlar) — saf karar; k = _kullanimlar çıktısı."""
    liste = [o for o in liste if not o.get("dolgu")]  # dolgu denetime girmez, devam turu açtırmaz
    yok = [o["ad"] for o in liste if not _kullanildi(o, k)]
    durum = []
    if liste and len(yok) >= min(3, math.ceil(len(liste) / 2)):
        durum.append("arac_eksik")
    if gorsel and not any("gorsel_hakem" in c for c in k[3]):
        durum.append("kanit_eksik")
    if any("tara_hizli" in c for c in k[3]) and _tarama_basarisiz():
        durum.append("arac_eksik")  # TARAMA-HIZ-1: zaman aşımı = taranmadı = EKSİK
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
    "graphify": ("graphify", "sor2", "tara_hizli"),  # RAM-BEKCI-1: tam repo `graphify update .` yasak; tara_hizli.py çıktısı graphify gereksinimini karşılar
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
    g = gerekceli(ad, d["eksik"])  # gerekçeli atlama kullanılmış sayılır: yeniden koşu tetiklemez
    if g:
        n = len([o for o in z["araclar"] if not o.get("dolgu")])
        kalan = [e for e in d["eksik"] if e not in g]
        d.update(gerekceli=g, eksik=kalan)
        if not (n and len(kalan) >= min(3, math.ceil(n / 2))):
            d["durum"] = "+".join(x for x in d["durum"].split("+") if x != "arac_eksik" or d.get("cekirdek_eksik")) or "ok"
    if "kanit_eksik" in d["durum"] and gorsel_gerekceli(ad):  # DENETİM-AYAR-1: "görsel çıktı üretmedi" gerekçesi kanıt_eksik tetiklemez
        d["durum"] = "+".join(x for x in d["durum"].split("+") if x != "kanit_eksik") or "ok"
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


def kuru_kosu(saat):
    """Son <saat> saatteki işaretli denetimler yeni araçlar()/gorsel_gerek() kuralıyla yeniden karara girer.
    (işaretli, liste/görsel işareti kalkan, hiçbir işaret kalmayan=devam turu gereksiz)"""
    tsv = {s.split("\t")[0]: s.split("\t")[1] for s in (KOK / ".kos/kopru/ajan-sira.tsv").read_text(encoding="utf-8").splitlines()
           if "\t" in s and not s.startswith("#")}
    sinir = time.time() - saat * 3600
    isaretli, temiz, gereksiz = 0, [], []
    for p in sorted(SIRA.glob("*.denetim.json"), key=lambda p: p.stat().st_mtime):
        if p.stat().st_mtime < sinir:
            continue
        ad = p.name.split(".")[0]
        try:
            eski = json.loads(p.read_text(encoding="utf-8"))
            z = json.loads((SIRA / f"{ad}.zorunlu.json").read_text(encoding="utf-8"))
            k = _kullanimlar(json.loads((SIRA / f"{ad}.json").read_text(encoding="utf-8")).get("session_id"))
            metin = (KOK / tsv[re.sub(r"-a2?$", "", ad)]).read_text(encoding="utf-8")
        except (OSError, ValueError, KeyError):
            continue
        if k is None or not any(i in eski["durum"] for i in ISARET):
            continue
        isaretli += 1
        ar, g = araclar(metin), gorsel_gerek(metin)
        eski_l, yeni_l = karar(z["araclar"], z["gorsel"], k)[0], karar(ar, g, k)[0]
        if eski_l == "ok" or yeni_l != "ok":
            continue  # liste/görsel kaynaklı işaret yoktu ya da yeni kuralda da duruyor
        temiz.append(ad)
        yeni = _hesapla(ad, {**z, "araclar": ar, "gorsel": g}, k, False)
        if yeni["durum"] == "ok":
            gereksiz.append(ad)
    return isaretli, temiz, gereksiz


ISARET = ("arac_eksik", "kanit_eksik", "ogrenme_eksik")
OTURUM = Path.home() / ".claude/zorunlu"  # etkileşimli oturum listeleri: <sid>.json {araclar, muaf: {ad: gerekçe}, red: n}
MUAF_LOG = KOK / ".kos/kopru/zorunlu-muaf.jsonl"  # gerekçeli muafiyetler denetime düşer
RED_TAVAN = 2  # aynı oturumda en çok bu kadar red; sonra bitişe izin + rapor (sonsuz döngü yok)


def oturum_yaz(sid, metin):
    """Etkileşimli oturum için zorunlu liste (dolgu hariç) → OTURUM/<sid>.json; boş liste yazılmaz."""
    ar = [o for o in araclar(metin) if not o.get("dolgu")]
    if ar:
        OTURUM.mkdir(parents=True, exist_ok=True)
        (OTURUM / f"{sid}.json").write_text(json.dumps({"araclar": ar, "muaf": {}, "red": 0}, ensure_ascii=False), encoding="utf-8")
    return ar


def muaf_ekle(sid, ad, gerekce):
    """Aracı gerekçeyle muaf say; gerekçe boşsa ValueError. Satır MUAF_LOG'a düşer."""
    if not gerekce.strip():
        raise ValueError("gerekçe boş")
    yol = OTURUM / f"{sid}.json"
    o = json.loads(yol.read_text(encoding="utf-8"))
    o["muaf"][ad] = gerekce.strip()
    yol.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
    with MUAF_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"sid": sid, "ad": ad, "gerekce": gerekce.strip(), "t": int(time.time())}, ensure_ascii=False) + "\n")


def kapi(sid):
    """Stop kapısı: (karar, eksikler) — 'izin' (liste yok/tamam/red tavanı) ya da 'red'. Eşik: listedeki HER araç (muaf hariç)."""
    yol = OTURUM / f"{sid}.json"
    try:
        o = json.loads(yol.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "izin", []
    k = _kullanimlar(sid)
    if k is None:
        return "izin", []
    yok = [a["ad"] for a in o["araclar"] if a["ad"] not in o.get("muaf", {}) and not _kullanildi(a, k)]
    if not yok:
        return "izin", []
    if o.get("red", 0) >= RED_TAVAN:
        with (KOK / ".kos/kopru/arac-eksik-rapor.jsonl").open("a", encoding="utf-8") as f:  # sessiz kapanma yok: Desktop'a raporlanır
            f.write(json.dumps({"sid": sid, "eksik": yok, "t": int(time.time())}, ensure_ascii=False) + "\n")
        return "izin", yok
    o["red"] = o.get("red", 0) + 1
    yol.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
    return "red", yok


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
        durum, yok = karar(ar, gorsel_gerek(metin), k)
        say += 1
        eksik += durum != "ok"
        print(f"{p.stem}\t{len(ar)}\t{len(ar) - len(yok)}\t{durum}\t{tur_bul(kapsam(metin))[0]}\t{' '.join(o['ad'] for o in ar)}")
    print(f"toplam {say} · işaretlenen {eksik}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 3 and sys.argv[1] == "--oturum":  # --oturum <sid> "<görev metni>"
        print(", ".join(o["ad"] for o in oturum_yaz(sys.argv[2], sys.argv[3])) or "liste boş")
    elif len(sys.argv) > 4 and sys.argv[1] == "--muaf":  # --muaf <sid> <araç> "<gerekçe>"
        muaf_ekle(sys.argv[2], sys.argv[3], sys.argv[4])
        print("muaf kaydedildi")
    elif len(sys.argv) > 2 and sys.argv[1] == "--geri":
        geri(int(sys.argv[2]))
    elif len(sys.argv) > 2 and sys.argv[1] == "--kuru":  # --kuru <saat>: yeni kuralla yeniden değerlendirme
        _i, _t, _g = kuru_kosu(float(sys.argv[2]))
        print(f"son {sys.argv[2]} saat · işaretli {_i} · liste/görsel işareti kalkan {len(_t)} · gereksiz devam turu {len(_g)}: {' '.join(_g)}")
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
