"""KALİTE-3 (b): tetiksiz/kısa açıklamaları abonelikle `claude -p` toplu yeniden yazar (Batch API yerine).

Hedef: skill-denetim.tsv'de tetik_yok/aciklama_kisa/aciklama_yok olan kayıtlar, (ad, açıklama) çiftine göre tekil.
Parti başına 40-60 skill: JSON girdi (ad + açıklama + gövdenin ilk 60 satırı) → JSON çıktı (yeni açıklama).
Her 10 partide bir sonnet örneklem denetimi (anlam kaybı / yanlış tetik). Sonuç JSONL'e eklenir, yeniden başlatınca
yazılmış adlar atlanır. Canlı dosyalara yazmaz; uygulama onay betiğinin işi.
python tools/aciklama_yaz.py <cikti.jsonl> [--parti 50] [--en-fazla 30] [--ad a,b]
"""
import argparse, csv, json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_filo_denetim import TETIK, ayir  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
DENETIM = KOK / "docs" / "kutuphane" / "skill-denetim.tsv"
SORUN = ("tetik_yok", "aciklama_kisa", "aciklama_yok")
TAVAN = 1024
PENCERESIZ = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW
YAZ_ISTEM = (
    "You rewrite Agent Skill descriptions so Claude knows exactly when to load each skill.\n"
    "Input: a JSON array of {ad, aciklama, govde} (govde = first 60 lines of the skill body).\n"
    "For each item write a new description: first what the skill does (keep every fact from the old description), then "
    "concrete triggers starting with 'Use when ...' (in Turkish originals: '... işinde/istendiğinde kullan'). "
    f"At most {TAVAN} characters. Keep the ORIGINAL language of the old description (if empty, the body's language). "
    "Do not invent capabilities not in the body. Reply with ONLY a JSON array of {\"ad\": ..., \"aciklama\": ...}, same order.\n\n")
DENETIM_ISTEM = (
    "Audit rewritten Agent Skill descriptions. Input: JSON array of {ad, eski, yeni, govde}. For each, answer whether the new "
    "description loses meaning from the old one or adds a wrong/misleading trigger not supported by govde. Reply with ONLY a "
    "JSON array of {\"ad\": ..., \"sorun\": \"yok\"|\"anlam_kaybi\"|\"yanlis_tetik\", \"not\": short}.\n\n")


def hedefler(tsv=DENETIM):
    csv.field_size_limit(10**8)
    gorulen, out = set(), []
    with open(tsv, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if not any(s in r["sorunlar"] for s in SORUN):
                continue
            yol = Path(r["yol"])
            yol = yol / "SKILL.md" if yol.is_dir() else yol
            try:
                fm, govde = ayir(yol.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
            anahtar = (r["ad"], fm.get("description", ""))
            if anahtar in gorulen:
                continue
            gorulen.add(anahtar)
            out.append({"ad": r["ad"], "yol": str(yol), "aciklama": fm.get("description", ""),
                        "govde": "\n".join(govde.splitlines()[:60])})
    return out


def json_dizi(metin):
    """Model yanıtındaki ilk JSON dizisi (```json çiti olsa da)."""
    m = re.search(r"\[.*\]", metin, re.S)
    return json.loads(m.group(0)) if m else []


def gecerli(eski, yeni):
    return bool(yeni) and len(yeni) <= TAVAN and bool(TETIK.search(yeni)) and yeni.strip() != eski.strip()


def claude(istem, model, timeout=900):
    """Tek `claude -p`, istem stdin'den (Windows komut satırı sınırı). Araçsız, boş geçici klasörde.
    MCP ve skill listesi yüklenmez (saf metin işi): ENABLE_TOOL_SEARCH=false iken her çağrı ~900 MCP aracı +
    ~2000 skill listesini önek olarak taşıyor ve her oturum ~75 alt süreç / ~3-4 GB açıyordu."""
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_BASE_URL"}
    with tempfile.TemporaryDirectory(prefix="aciklama-", ignore_cleanup_errors=True) as bos:
        t = time.monotonic()
        r = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json", "--max-turns", "1",
                            # video/hafif.py A1 kalıbı (MOTOR-M2a): araçsız, ayar/hook/MCP/skill yüklemeden, oturum yazmadan
                            "--tools", "", "--setting-sources", "", "--strict-mcp-config", "--safe-mode",
                            "--disable-slash-commands", "--no-session-persistence",
                            "--disallowedTools", "Bash,Edit,Write,Read,Glob,Grep,WebFetch,WebSearch,Task,Agent"],
                           input=istem, capture_output=True, encoding="utf-8", errors="replace", env=env, cwd=bos,
                           timeout=timeout, creationflags=PENCERESIZ)
    try:
        j = json.loads(r.stdout)
    except json.JSONDecodeError:
        j = {"result": "", "is_error": True}
    return j.get("result", ""), round(time.monotonic() - t, 1), j.get("total_cost_usd", 0), r.returncode


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cikti")
    ap.add_argument("--parti", type=int, default=50)
    ap.add_argument("--en-fazla", type=int, default=30, help="bu koşuda en fazla claude -p çağrısı (denetim dahil)")
    ap.add_argument("--ad", help="virgüllü ad süzgeci (pilot)")
    a = ap.parse_args()
    cikti = Path(a.cikti)
    yapildi = {json.loads(s)["ad"] for s in cikti.read_text(encoding="utf-8").splitlines() if s.strip()} if cikti.exists() else set()
    is_ = [h for h in hedefler() if h["ad"] not in yapildi and (not a.ad or h["ad"] in a.ad.split(","))]
    print(f"hedef {len(is_)} (yapılmış {len(yapildi)})", flush=True)
    cagri, parti_no = 0, len(yapildi) // a.parti
    for i in range(0, len(is_), a.parti):
        if cagri >= a.en_fazla:
            break
        parti = is_[i:i + a.parti]
        girdi = [{"ad": h["ad"], "aciklama": h["aciklama"], "govde": h["govde"]} for h in parti]
        metin, sure, usd, rc = claude(YAZ_ISTEM + json.dumps(girdi, ensure_ascii=False), "haiku")
        cagri, parti_no = cagri + 1, parti_no + 1
        try:
            yeni = {d["ad"]: d.get("aciklama", "") for d in json_dizi(metin)}
        except json.JSONDecodeError:
            yeni = {}
        satirlar = [{"ad": h["ad"], "yol": h["yol"], "eski": h["aciklama"], "yeni": yeni.get(h["ad"], ""),
                     "gecerli": gecerli(h["aciklama"], yeni.get(h["ad"], "")), "parti": parti_no} for h in parti]
        ok = sum(s["gecerli"] for s in satirlar)
        denetim = ""
        if parti_no % 10 == 1 and cagri < a.en_fazla:  # 1., 11., 21. parti: sonnet örneklem
            orn = [s for s in satirlar if s["gecerli"]][:10]
            govde = {h["ad"]: h["govde"][:1200] for h in parti}
            d, _, usd2, _ = claude(DENETIM_ISTEM + json.dumps([{"ad": s["ad"], "eski": s["eski"], "yeni": s["yeni"],
                                                                "govde": govde[s["ad"]]} for s in orn], ensure_ascii=False), "sonnet")
            cagri, usd = cagri + 1, usd + usd2
            try:
                bul = {x["ad"]: x for x in json_dizi(d)}
            except json.JSONDecodeError:
                bul = {}
            for s in satirlar:
                if s["ad"] in bul:
                    s["denetim"] = bul[s["ad"]].get("sorun", "?")
                    s["denetim_not"] = bul[s["ad"]].get("not", "")
            denetim = f" · sonnet {sum(x.get('sorun') == 'yok' for x in bul.values())}/{len(orn)} temiz"
        with open(cikti, "a", encoding="utf-8", newline="\n") as f:
            for s in satirlar:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        print(f"parti {parti_no}: {ok}/{len(parti)} geçerli · {sure}s · ${usd:.4f} · rc {rc}{denetim}", flush=True)
    print(f"bitti: {cagri} çağrı", flush=True)


if __name__ == "__main__":
    main()
