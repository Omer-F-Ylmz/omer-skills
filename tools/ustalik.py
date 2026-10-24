"""USTALIK-1: kurulu araçların kullanım kartları + küçük deneme (model yok, $0).
  python -I tools/ustalik.py sirala              -> .kos/kopru/ara/ustalik-sira.tsv (parça no ile)
  python -I tools/ustalik.py kart <parca>        -> kartlar/arac/<ad>.md + Obsidian 30-araclar/ + deneme sonucu
  python -I tools/ustalik.py tur                 -> tur_setleri.json'a "fikir-karar" türünü ekler
Sır değeri okunmaz: ~/.claude.json'dan yalnız MCP command/args/url alınır, env atılır."""
import csv, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HOME = Path.home()
SIRA = KOK / ".kos/kopru/ara/ustalik-sira.tsv"
SONUC = KOK / ".kos/kopru/ara/ustalik-deneme.tsv"
KART = KOK / "kartlar/arac"
KASA = Path(r"C:\Users\pc\Desktop\Obsidian") / "30-araclar"
PARCA = 100
CEKIRDEK = [("graphify", "skill"), ("headroom-compress", "skill"), ("strategic-compact", "skill"),
            ("claude-mem", "mcp"), ("context-mode", "mcp"), ("rtk", "cli"), ("headroom", "cli"),
            ("beyin", "cli"), ("ruflo", "cli")]


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def satirlar():
    with open(KOK / "docs/envanter/envanter.tsv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def sirala():
    r = [x for x in satirlar() if x["tur"] in ("mcp", "cli") and x["nerede"] != "yok" and "skills-cli" not in x["ad"] and norm(x["ad"])]
    r.sort(key=lambda x: x["son_kullanim"][-10:], reverse=True)  # son kullanılan önce
    gor, cikti = set(), []
    for ad, tur in CEKIRDEK:
        gor.add(ad); cikti.append((ad, tur))
    for x in r:
        if x["ad"] in gor or x["ad"].startswith("plugin:"):
            continue
        gor.add(x["ad"]); cikti.append((x["ad"], x["tur"]))
    SIRA.parent.mkdir(parents=True, exist_ok=True)
    with open(SIRA, "w", encoding="utf-8", newline="\n") as f:
        f.write("parca\tad\ttur\n")
        for i, (ad, tur) in enumerate(cikti):
            f.write(f"{i // PARCA + 1}\t{ad}\t{tur}\n")
    print(len(cikti), "araç,", (len(cikti) + PARCA - 1) // PARCA, "parça")


def mcp_ayar():
    """ad -> (command, args|url); env okunmaz"""
    s = {}
    try:
        d = json.load(open(HOME / ".claude.json", encoding="utf-8"))
    except Exception:
        d = {}
    kaynak = [d.get("mcpServers", {})] + [p.get("mcpServers", {}) for p in d.get("projects", {}).values()]
    for p in (HOME / ".claude/plugins").rglob(".mcp.json"):
        try:
            j = json.load(open(p, encoding="utf-8"))
            kaynak.append(j.get("mcpServers", j))
        except Exception:
            pass
    for k in kaynak:
        for ad, v in k.items():
            if isinstance(v, dict):
                s.setdefault(ad, (v.get("command") or v.get("url") or "", v.get("args", [])[:2], v.get("type", "")))
    return s


def calistir(komut, sure=8):
    # boru yerine geçici dosya + ağaç öldürme: torun süreç boruyu tutup zaman aşımını asıyordu (inspector)
    with tempfile.TemporaryFile() as cikti:
        p = subprocess.Popen(komut, stdout=cikti, stderr=subprocess.STDOUT, env=dict(os.environ),
                             stdin=subprocess.DEVNULL, creationflags=0x08000000)
        try:
            rc = p.wait(timeout=sure)
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True, timeout=10,
                           env=dict(os.environ))
            return 98, "zaman aşımı"
        cikti.seek(0)
        return rc, cikti.read().decode("utf-8", "replace").strip()


def cli_bin(ad):
    return ad.split("/")[-1].removesuffix("-mcp") if ad.startswith("@") else ad


_YER = {}


def yerler():
    """kurulum yerleri: ad(norm) -> yol. npm global, uv tool, npx önbelleği, eklenti önbelleği, skill dizini"""
    if _YER:
        return _YER
    kokler = [Path(os.environ.get("APPDATA", "")) / "npm/node_modules", Path(os.environ.get("APPDATA", "")) / "uv/tools",
              HOME / ".local/share/uv/tools", HOME / ".claude/skills"]
    kokler += list((HOME / ".npm/_npx").glob("*/node_modules")) + list((HOME / ".claude/plugins/cache").glob("*/*"))
    kokler += list((HOME / ".claude/plugins/cache").glob("*/*/*"))
    kokler += list((HOME / ".claude/plugins/cache").glob("*/*/*/skills")) + [HOME / ".claude/plugins/cache"]
    kokler += list((HOME / ".claude/plugins/cache").glob("*/*"))  # eklenti adı = ikinci düzey dizin
    for k in kokler:
        if not k.is_dir():
            continue
        for d in k.iterdir():
            if d.name.startswith("@") and d.is_dir():
                for e in d.iterdir():
                    _YER.setdefault(norm(d.name + e.name), d)
                    _YER.setdefault(norm(e.name), e)
            else:
                _YER.setdefault(norm(d.name), d)
    return _YER


def varlik(ad):
    y = yerler()
    for a in (ad, ad.split("/")[-1], ad.removesuffix("-cli").removesuffix("-mcp")):
        if norm(a) in y:
            return str(y[norm(a)]).replace(str(HOME), "~")
    return ""


# kurulum adı -> PATH'teki komut adı (paket adından türetilemeyenler)
ALIAS = {"netlify-cli": "netlify", "open-code-review": "ocr", "testsprite-cli": "testsprite",
         "ecc-agentshield": "agentshield", "puppeteer-mcp-server": "mcp-server-puppeteer",
         "ui-to-vue-converter": "ui-to-vue", "headroom-ai": "headroom", "jev-cli": "jev", "video-cli": "video",
         "graphifyy": "graphify", "mimic-client": "mimic", "strix-agent": "strix", "whisper-cli": "whisper",
         "@googleworkspace/cli": "gws", "@larksuite/cli": "lark-cli", "@gltf-transform/cli": "gltf-transform",
         "@playwright/cli": "playwright-cli", "@caveman-ai/cli": "caveman"}
# kalıcı koşturulamayanlar: ad -> gerekçe (kapı hesabı dışı)
MUAF = {"skill-ui": "npm'den kaldırılmış (2023-04-28), global kurulum dizini boş; kaynak depo bilinmiyor, yeniden kurulamaz",
        "open-design": "`od` komutu Open Design masaüstü uygulamasıyla gelir, uygulama kurulu değil; daemon 127.0.0.1:7456 gerekir",
        "whisper-cli": "whisper.cpp ikilisi kurulu değil (yalnız cc-kopru izin adı); çalışan ASR yolu tools/asr_hat.py (groq→gemini→faster-whisper)"}
BAYRAK = ("--version", "-V", "version", "--help", "-h", "help")


def eklenti_mcp(ad):
    """eklenti önbelleğindeki .mcp.json / plugin.json'dan (komut, args); ${CLAUDE_PLUGIN_ROOT} açılır"""
    for kok in (HOME / ".claude/plugins/cache").glob(f"*/{ad}/*"):
        for dosya in (kok / ".mcp.json", kok / ".claude-plugin/plugin.json"):
            if not dosya.exists():
                continue
            d = json.loads(dosya.read_text(encoding="utf-8"))
            for v in (d.get("mcpServers") or d).values():
                if isinstance(v, dict) and v.get("command"):
                    return v["command"], [str(a).replace("${CLAUDE_PLUGIN_ROOT}", str(kok)) for a in v.get("args", [])]
    return None


def mcp_tools(komut, args):
    """MCP stdio'yu gerçekten başlatır: initialize + tools/list; araç sayısı ya da hata metni"""
    istek = "\n".join(json.dumps(m) for m in (
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                                                                       "clientInfo": {"name": "ustalik", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})) + "\n"
    try:
        p = subprocess.run([shutil.which(komut) or komut] + args, input=istek.encode(), capture_output=True, timeout=45,
                           env=dict(os.environ), creationflags=0x08000000)
    except Exception as e:
        return None, str(e)[:80]
    for satir in p.stdout.decode("utf-8", "replace").splitlines():
        if '"id":2' in satir.replace(" ", "") and '"tools"' in satir:
            return len(json.loads(satir)["result"]["tools"]), ""
    return None, (p.stderr.decode("utf-8", "replace").strip()[:80] or "tools/list yanıtı yok")


def deneme(ad, tur, mcp):
    if tur == "skill" and (HOME / ".claude/skills" / ad).is_dir():
        return "GECTI", f"SKILL.md ~/.claude/skills/{ad}", "skill dizini var"
    if tur == "mcp":
        c = eklenti_mcp(ad) or eklenti_mcp(ad.split("-mcp")[0])
        if c:
            n, hata = mcp_tools(*c)
            if n:
                return "GECTI", f"{c[0]} (stdio) tools/list", f"{n} araç döndü"
            return "VAR", f"{c[0]} (stdio) tools/list", hata
    if tur == "cli":
        b = ALIAS.get(ad) or ALIAS.get(cli_bin(ad))
        yol = b and shutil.which(b)
        if not yol:
            ilk = _deneme_ilk(ad, tur, mcp)
            if ilk[0] != "VAR":
                return ilk
            yol = next((shutil.which(x) for x in (ALIAS.get(ad), cli_bin(ad), ad.split("/")[-1]) if x and shutil.which(x)), None)
            b = b or cli_bin(ad)
        if yol:
            on = [] if yol.lower().endswith((".exe", ".cmd", ".bat")) else ["sh"]
            for bayrak in BAYRAK:
                rc, cikti = calistir(on + [yol, bayrak], sure=45 if bayrak in BAYRAK[:1] else 12)
                if rc == 0:
                    return "GECTI", f"{b} {bayrak}", (cikti.splitlines() or [""])[0][:100]
            return "VAR", f"{b} --version", f"yürütülebilir {yol}, yanıt yok (rc={rc})".replace(str(HOME), "~")
    return _deneme_ilk(ad, tur, mcp)


def _deneme_ilk(ad, tur, mcp):
    """(durum, komut, not); durum GECTI = koştu, VAR = kurulu yer bulundu ama sürüm yanıtı yok/komut PATH dışı, KALDI"""
    if tur == "skill":
        v = varlik(ad)
        return ("GECTI", f"SKILL.md {v}", "skill dizini var") if v else ("KALDI", ad, "skill dizini yok")
    if tur == "mcp":
        c = mcp.get(ad) or mcp.get(ad.replace("-mcp", ""))
        if c:
            komut, arg, tip = c
            if komut.startswith("http"):
                return "GECTI", f"url {komut.split('?')[0]}", "uzak MCP; yapılandırma var (bağlantı sınanmadı)"
            yol = shutil.which(komut)
            if yol:
                return "GECTI", f"{komut} {' '.join(arg)}".strip(), "yürütülebilir bulundu"
        v = varlik(ad)
        if v:
            return "VAR", f"npx/uvx {ad}", f"kurulu yer {v}; yapılandırmada ayrı ad"
        return "KALDI", ad, "yapılandırmada ve kurulu yerde yok"
    for b in dict.fromkeys([cli_bin(ad), ad.split("/")[-1]]):
        yol = shutil.which(b)
        if yol:
            on = [] if yol.lower().endswith((".exe", ".cmd", ".bat")) else ["sh"]
            for bayrak in ("--version", "--help", "-h"):
                rc, cikti = calistir(on + [yol, bayrak])
                if rc == 0:
                    return "GECTI", f"{b} {bayrak}", (cikti.splitlines() or [""])[0][:100]
            return "VAR", f"{b} --version", f"yürütülebilir {yol}, yanıt yok (rc={rc})".replace(str(HOME), "~")
    v = varlik(ad)
    if v:
        return "VAR", f"npx -y {ad}", f"PATH dışı, kurulu yer {v}"
    return "KALDI", f"{cli_bin(ad)} --version", "PATH'te ve kurulu yerlerde yok"


def video_notlari(ad, arac):
    """arac-tam.tsv'den video kodları + ilk 3 videoda aracın geçtiği satırlar"""
    n = norm(ad.split("/")[-1])
    kodlar, ref = [], ""
    for x in arac:
        if x["norm"] == n:
            say, _, k = x["video_say:kodlar"].partition(":")
            kodlar, ref = k.split(","), say
            break
    ipuc = []
    for k in kodlar[:4]:
        p = KOK / "docs/video-tarama" / f"{k}.md"
        if not p.exists():
            continue
        for s in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if ad.split("/")[-1].lower() in s.lower() and 25 < len(s) < 260:
                ipuc.append(f"- ({k}) {s.strip()}")
                break
    return ref, kodlar, ipuc[:3]


def kart(ad, tur, satir, mcp, arac, tur_set):
    durum, komut, nota = deneme(ad, tur, mcp)
    if ad in MUAF and durum != "GECTI":
        nota = f"{nota}; ÖMER: {MUAF[ad]}"
        durum = "MUAF"
    ok = durum not in ("KALDI", "MUAF")
    ref, kodlar, ipuc = video_notlari(ad, arac)
    zor = [t for t, v in tur_set.items() if ad in v.get("mcp", []) + v.get("cli", []) + v.get("skill", [])]
    ortak = sorted({o for t in zor for k in ("skill", "mcp", "cli") for o in tur_set[t].get(k, []) if o != ad})[:8]
    oz = (satir or {}).get("ozellik", "").strip() or "(envanterde açıklama yok)"
    cek = ad in [a for a, _ in CEKIRDEK]
    govde = f"""---
type: arac-karti
status: {'dogrulandi' if durum == 'GECTI' else ('muaf' if durum == 'MUAF' else ('kurulu-kosmadi' if ok else 'onarim'))}
tags: [arac, {tur}, ustalik-1]
relatedTo: [kurulum, tur-setleri]
---
# {ad} ({tur})
- **Ne işe yarar:** {oz[:300]}
- **ZORUNLU iş türü:** {'her iş (çekirdek)' if cek else (', '.join(zor) if zor else 'türe bağlı değil; yan fayda')}. Küçük iş/düşünme anı: tek karar/fikir varsa önce idea-refine·doubt-driven-development ile sına, araç gerekiyorsa buradan seç.
- **Tetik kelimeler:** {ad}, {', '.join(sorted({w for t in zor for w in [t]})) or '-'}
- **En iyi kullanım:** {'videolarda ' + ref + ' kez anıldı; ilk kodlar: ' + ', '.join(kodlar[:4]) if kodlar else 'videoda anılmıyor (kaynak: envanter/yapılandırma)'}
{chr(10).join(ipuc) if ipuc else '- (videodan alıntı satırı bulunamadı)'}
- **Kombin ortakları:** {', '.join(ortak) or '-'}
- **Yaygın hata:** {'PATH/yapılandırmada bulunamadı: ' + nota if not ok else 'sunucuyu/komutu çıktı değerlerini (anahtar, env) basmadan çağır; sınama yalnız sürüm/yürütülebilir'}
- **Doğrulanmış örnek:** `{komut}`  → {durum} ({nota})
"""
    return durum, govde, komut, nota


def kartlar(parca):
    arac = list(csv.DictReader(open(KOK / ".kos/kopru/rapor/arac-tam.tsv", encoding="utf-8"), delimiter="\t"))
    tur_set = json.load(open(KOK / "tools/tur_setleri.json", encoding="utf-8"))["turler"]
    env = {(x["ad"], x["tur"]): x for x in satirlar()}
    mcp = mcp_ayar()
    KART.mkdir(parents=True, exist_ok=True); KASA.mkdir(parents=True, exist_ok=True)
    gecen, var, muaf, kalan = 0, 0, 0, []
    rows = [l.split("\t") for l in SIRA.read_text(encoding="utf-8").splitlines()[1:]]
    with open(SONUC, "w", encoding="utf-8", newline="\n") as sf:
        for p, ad, tur in rows:
            if p != str(parca):
                continue
            durum, govde, komut, nota = kart(ad, tur, env.get((ad, tur)), mcp, arac, tur_set)
            dosya = re.sub(r"[^\w.-]", "_", ad) + ".md"
            for d in (KART, KASA):
                (d / dosya).write_bytes(govde.encode("utf-8"))
            sf.write(f"{parca}\t{ad}\t{tur}\t{durum}\t{komut}\t{nota}\n")
            muaf += durum == "MUAF"
            gecen += durum == "GECTI"
            var += durum == "VAR"
            if durum == "KALDI":
                kalan.append(ad)
    kapi = gecen + var + len(kalan)  # muaf kartlar kapı hesabından çıkar
    print(f"parça {parca}: kart {kapi + muaf}, koştu-geçti {gecen}, kurulu-koşmadı {var}, muaf {muaf}, kalan {len(kalan)}: {kalan}; "
          f"kapı %{100 * gecen / max(kapi, 1):.1f}")


def tur_ekle():
    yol = KOK / "tools/tur_setleri.json"
    d = json.loads(yol.read_text(encoding="utf-8"))
    d["turler"]["fikir-karar"] = {"skill": ["idea-refine", "brainstorming", "interview-me", "doubt-driven-development",
                                            "gstack-plan-ceo-review", "gstack-office-hours", "design-critique"],
                                  "mcp": [], "cli": []}
    d["desen"]["fikir-karar"] = r"(?i)\b(fikir\w*|karar\w*|idea|decision|öneri\w*|strateji\w*|plan\w*)\b"
    yol.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("fikir-karar eklendi")


if __name__ == "__main__":
    {"sirala": sirala, "kart": lambda: kartlar(sys.argv[2]), "tur": tur_ekle}[sys.argv[1]]()
