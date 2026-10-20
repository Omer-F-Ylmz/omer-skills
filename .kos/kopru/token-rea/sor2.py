"""sor2: graphify hibrit sorgu. graph.json'u süreç içinde okur (CLI/ağır başlangıç yok), dosya yolu+etiket eşleşmesiyle ≤1.5k token verir.
  python sor2.py "soru"     |  python sor2.py egitim|held  → sor2_ab_<mod>.json (held tek sefer; kilit sor2_held.lock)"""
import hashlib, json, math, os, re, sys, time
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
        g = json.load((KOK / "graphify-out/graph.json").open(encoding="utf-8"))
        m = (KOK / "graphify-out/graph.json").stat().st_mtime
        ön = KOK / "graphify-out/sor2_belge.json"  # dosya başı docstring/yorum (ilk 600 kr), graph mtime'a bağlı önbellek
        if ön.exists() and (c := json.load(ön.open(encoding="utf-8")))["m"] == m:
            _G["b"] = c["d"]
        else:
            _G["b"] = {}
            for f in {n.get("source_file", "").lower() for n in g["nodes"]}:
                try: _G["b"][f] = (KOK / f).read_text(encoding="utf-8", errors="ignore")[:600].lower()
                except OSError: pass
            json.dump({"m": m, "d": _G["b"]}, ön.open("w", encoding="utf-8"), ensure_ascii=False)
        _G["n"] = [(n.get("norm_label") or n["label"].lower(), n.get("source_file", "").lower(), n["label"], n.get("source_location", "")) for n in g["nodes"]]
    return _G["n"]


def sor(soru, kap_kr=4500):
    N = yukle()
    w = [x[:6] for x in re.findall(r"\w{3,}", soru.lower().replace("_", " ")) if x not in STOP] + re.findall(r"\w+_\w+", soru.lower())
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
    if sys.argv[1] not in ("egitim", "held", "held2"):
        sys.stdout.buffer.write(sor(sys.argv[1]).encode("utf-8")); raise SystemExit
    import taban as t
    mod, liste = sys.argv[1], {"egitim": EGITIM, "held": HELD, "held2": HELD2}[sys.argv[1]]
    if mod == "held2":
        assert hashlib.sha256(json.dumps(HELD2).encode()).hexdigest() == (t.BU / "sor2_held2.lock").read_text().strip(), "held-out değişmiş"
    os.chdir(KOK); t.GOVDE, t.BASLIK = t.kur_baslik()
    sat = []
    for q, k in liste:
        ts = time.time(); c = sor(q); s = time.time() - ts
        cg, tg, _ = t.kos(["graphify", "query", q], tmo=90)
        sat.append({"ad": q, "tok": t.tok(c), "sn": round(s, 2), "hit": int(k.lower() in c.lower()), "g_tok": t.tok(cg), "g_sn": round(tg, 2), "g_hit": int(k.lower() in cg.lower())})
    top = {k: round(sum(x[k] for x in sat), 2) for k in sat[0] if k != "ad"}
    print(mod, "n", len(sat), top)
    for x in sat:
        if not x["hit"]: print("  !", x["ad"])
    json.dump({"satir": sat, "toplam": top}, open(t.BU / f"sor2_ab_{mod}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
