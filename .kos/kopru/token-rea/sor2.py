"""sor2: graphify hibrit sorgu. graph.json'u süreç içinde okur (CLI/ağır başlangıç yok), dosya yolu+etiket eşleşmesiyle ≤1.5k token verir.
  python sor2.py "soru"     |  python sor2.py egitim|held  → sor2_ab_<mod>.json (held tek sefer; kilit sor2_held.lock)"""
import hashlib, json, math, os, pickle, re, subprocess, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
EGITIM = [("token_olc ağırlıklı ölçüm", "token_olc"), ("cc_profil kur", "cc_profil"), ("onek_kayit vekil", "onek_kayit"),
          ("ucuz_alt free zincir", "ucuz_alt"), ("beyin kapı doğru", "beyin"), ("mem_bekci sağlık", "mem_bekci"),
          ("graphify_sor etiket", "graphify_sor"), ("nblm paket", "nblm"), ("zip_denetle", "zip_denetle"), ("kapi_kos ters", "kapi_kos")]
HELD = [("günün dalga ilerlemesini gösteren durum özeti", "dalga_durum"), ("headroom vekilinin claude isteklerini koruyan bekçi", "headroom_claude_guard"),
        ("rtk için komut öncesi ön işleme", "rtk_onisle"), ("ajanları sıraya dizen çizelge", "ajan_sira"), ("model hızını ve maliyetini ölçen betik", "model_olc")]
HELD2 = [("komutları rtk ile yeniden yazan kanca", "rtk_onisle"), ("ücretsiz modelleri sırayla deneyen havuz", "ucretsiz_havuz"),
         ("Claude Code ayar profili yazan araç", "cc_profil"), ("günlük durumun kısa özetini çıkaran betik", "durum_ozet"),
         ("Claude'u tek seferlik çağıran sarmalayıcı", "claude_bak"), ("paket zip'inde sızıntı arayan denetim", "zip_denetle"),
         ("girdi jetonu sayımını yapan betik", "token_olc"), ("değişikliği yedekli uygulayan yama aracı", "yamala")]  # d4 held-out, kilit sor2_held2.lock
SYN = {k[:6]: v[:6] for k, v in {"durum": "status", "özet": "summary", "ölçüm": "measure", "ölçen": "measure", "sıra": "queue", "bekçi": "guard", "kapı": "gate",
       "sağlık": "health", "sorgu": "query", "hafıza": "memory", "bellek": "memory", "önbellek": "cache", "komut": "command", "yama": "patch",
       "çizelge": "schedule", "kanca": "hook", "sarmalayıcı": "wrapper", "denetim": "audit", "sızıntı": "leak", "jeton": "token", "ayar": "config"}.items()}
STOP = {"için", "olan", "gibi", "yapan", "eden", "ile"}
_G = {}


def yukle():
    if not _G:
        gj = KOK / "graphify-out/graph.json"
        m = gj.stat().st_mtime
        pk = KOK / "graphify-out/sor2_dizin.pkl"  # ayrıştırılmış dizin (etiket/dosya/yer + docstring + bayat dosya metni), graph mtime'a bağlı; 40 MB json okumayı atlar
        try:
            with pk.open("rb") as f: c = pickle.load(f)
            if c["m"] != m: raise ValueError
        except (OSError, ValueError, KeyError, pickle.UnpicklingError, EOFError):
            g = json.load(gj.open(encoding="utf-8"))
            c = {"m": m, "b": {}, "s": {}, "n": [(n.get("norm_label") or n["label"].lower(), n.get("source_file", "").lower(), n["label"], n.get("source_location", "")) for n in g["nodes"]]}
            for f in {n.get("source_file", "").lower() for n in g["nodes"]}:
                try: c["b"][f] = (KOK / f).read_text(encoding="utf-8", errors="ignore")[:600].lower()
                except OSError: pass
            c["kirli"] = True
        _G["n"], _G["b"] = list(c["n"]), dict(c["b"])
        bayat_ekle(m, c)
        if c.pop("kirli", False):
            tmp = pk.with_suffix(".tmp")
            with tmp.open("wb") as f: pickle.dump(c, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, pk)
    return _G["n"]


def bayat_ekle(m, c):
    """Bayatlık denetimi: graph.json'dan yeni/izlenmeyen ya da sonradan değişen .py dosyaları düz metin dizinine girer (o sorguda yedek arama);
    bayat varsa `graphify update .` arka.py ile (CREATE_NO_WINDOW) başlatılır, 10 dk'da bir."""
    bilinen = {f for _, f, *_ in _G["n"]}
    # git ls-files -o bu depoda 0.7 sn: yerine grafın bildiği kök dizinlerde scandir (shortcut: grafta hiç olmayan yeni kök dizin görülmez, graphify update onu yakalar)
    atla, bayat, kokler = {"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "graphify-out"}, [], {f.split("/")[0] for f in bilinen if "/" in f}

    def gez(d, derin=0):  # shortcut: 4 düzeyden derin dosya görülmez (14k dizinli ağaçta tam gezi 0.6 sn), graphify update yakalar
        for e in os.scandir(d):
            if e.is_dir(follow_symlinks=False):
                if e.name not in atla and derin < 4: gez(e.path, derin + 1)
            elif e.name.endswith(".py") and ((f := os.path.relpath(e.path, KOK).replace("\\", "/")).lower() not in bilinen or e.stat().st_mtime > m):
                bayat.append((f, e.stat().st_mtime))
    for k in kokler:
        if (KOK / k).is_dir(): gez(KOK / k)
    for f, mt in bayat:
        fl = f.lower()
        if fl not in c["s"] or c["s"][fl][0] != mt:  # bayat dosya metni (mtime, metin) önbellekte; yalnız değişen yeniden okunur
            try: c["s"][fl] = (mt, (KOK / f).read_text(encoding="utf-8", errors="ignore")[:600].lower()); c["kirli"] = True
            except OSError: continue
        _G["b"][fl] = c["s"][fl][1]
        if fl not in bilinen:
            _G["n"].append((Path(f).stem.lower(), fl, Path(f).stem, ""))
    isaret = KOK / "graphify-out/.sor2_guncelleme"
    if bayat and not (isaret.exists() and time.time() - isaret.stat().st_mtime < 600):
        isaret.write_text("1"); subprocess.run([sys.executable, str(KOK / ".kos/kopru/arka.py"), ".kos/kopru/token-rea/_graf_guncelle.log",
                                                 ".kos/kopru/token-rea/graf_guncelle.py"], cwd=KOK, creationflags=0x08000000, capture_output=True)


def genis(soru):
    """Havuzla sorgu genişletme: tek kısa çağrı, graphify-out/sor2_genis.json'da önbellek; havuz yoksa boş."""
    ön = KOK / "graphify-out/sor2_genis.json"
    c = json.load(ön.open(encoding="utf-8")) if ön.exists() else {}
    k = hashlib.sha1(soru.encode()).hexdigest()[:12]
    if k not in c:
        sys.path.insert(0, str(KOK / "tools")); import ucretsiz_havuz as H
        y, *_ = H.cagir("ozet", "Bir kod deposunda şu soruya cevap veren betiği bulmak için aranacak 10 anahtar sözcük yaz: Türkçe ve İngilizce eş anlamlılar, "
                        "olası dosya adı parçaları. Yalnız virgülle ayrılmış sözcükler.\nSoru: " + soru, max_tokens=120, haiku_tavan=0, etiket="sor2-genis", zaman=20)
        if not y: return ""
        c[k] = y.strip()[:300]; json.dump(c, ön.open("w", encoding="utf-8"), ensure_ascii=False)
    return c[k]


def sor(soru, kap_kr=4500, ek=False):
    N = yukle()
    w = [x[:6] for x in re.findall(r"\w{3,}", soru.lower().replace("_", " ")) if x not in STOP] + re.findall(r"\w+_\w+", soru.lower())
    if ek: w += [x[:6] for x in re.findall(r"\w{3,}", genis(soru).lower().replace("_", " ")) if x not in STOP]
    w += [SYN[x] for x in w if x in SYN]  # 6 kr kök: Türkçe ek toleransı; alt çizgili ad bütün
    df = {x: sum(1 for l, f, *_ in N if x in l or x in f) or 1 for x in w}
    agirlik = {x: math.log(len(N) / df[x]) * (3 if "_" in x else 1) for x in w}
    dosya = {}
    for l, f, ad, yer in N:
        s = sum(agirlik[x] * (2 if x in f else 1) for x in w if x in l or x in f)
        if s:
            d = dosya.setdefault(f, [0, []])
            d[0] += s
            d[1].append((s, ad, yer))
    for f, tx in _G["b"].items():  # belge eşleşmesi: docstring'de geçen kökler dosyayı etiketi olmasa da öne çıkarır
        b = sum(agirlik[x] for x in w if x in tx)
        if b:
            dosya.setdefault(f, [0, []]).append(1.5 * b)
    cik, top = [], 0
    for f, (s, lst, *bb) in sorted(dosya.items(), key=lambda kv: -(sum(sorted((x[0] for x in kv[1][1]), reverse=True)[:3]) + sum(kv[1][2:])))[:8]:
        lst.sort(key=lambda t: -t[0])
        satir = f"{f}: " + (", ".join(f"{a}{y}" for _, a, y in lst[:3]) or _G["b"][f][:60].replace("\n", " "))
        if top + len(satir) > kap_kr:
            break
        cik.append(satir); top += len(satir)
    return "\n".join(cik)


if __name__ == "__main__":
    if sys.argv[1] not in ("egitim", "held", "held2", "heldout"):
        sys.stdout.buffer.write(sor(sys.argv[1], ek="--genis" in sys.argv).encode("utf-8")); raise SystemExit
    import taban as t
    mod = sys.argv[1]
    if mod == "heldout":  # heldout <tohum>: heldout_uret.py üretir; tek sefer, kilit doğrulanır, kaçanların adı BASILMAZ
        mod = "heldout_" + sys.argv[2]; kap = t.BU / "heldout"
        liste = json.load((kap / f"sor2_{sys.argv[2]}.json").open(encoding="utf-8"))
        assert hashlib.sha256(json.dumps(liste, ensure_ascii=False).encode()).hexdigest() == (kap / f"sor2_{sys.argv[2]}.lock").read_text().strip(), "held-out değişmiş"
    else:
        liste = {"egitim": EGITIM, "held": HELD, "held2": HELD2}[mod]
        if mod == "held2":
            assert hashlib.sha256(json.dumps(HELD2).encode()).hexdigest() == (t.BU / "sor2_held2.lock").read_text().strip(), "held-out değişmiş"
    os.chdir(KOK); t.GOVDE, t.BASLIK = t.kur_baslik()
    sat = []
    for q, k in liste:
        ts = time.time(); c = sor(q); s = time.time() - ts
        c2 = sor(q, ek=True)  # genişletmeli kol: havuz çağrısı süresi ayrı raporlanır (önbellekli ikinci koşuda ~0)
        cg, tg, _ = t.kos(["graphify", "query", q], tmo=90)
        sat.append({"ad": q, "tok": t.tok(c), "sn": round(s, 2), "hit": int(k.lower() in c.lower()), "ek_tok": t.tok(c2), "ek_hit": int(k.lower() in c2.lower()),
                    "g_tok": t.tok(cg), "g_sn": round(tg, 2), "g_hit": int(k.lower() in cg.lower())})
    top = {k: round(sum(x[k] for x in sat), 2) for k in sat[0] if k != "ad"}
    print(mod, "n", len(sat), top)
    if not mod.startswith("heldout") or "egit" in mod:  # tohumu "egit…" olan set geliştirme içindir, okunabilir
        for x in sat:
            if not x["hit"]: print("  !", x["ad"])
    json.dump({"satir": sat, "toplam": top}, open(t.BU / f"sor2_ab_{mod}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
