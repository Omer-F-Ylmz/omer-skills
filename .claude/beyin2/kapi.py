"""BEYIN-2 d2 kapı: aynı 40 soru (tohum 2005/2006, 20+20, tohum başına 10 çok-notlu).
A = beyin yolu (yalnız Bash `beyin.py ara`), B = dosya okuma yolu (yalnız Read). İkisi aynı düzenek, aynı taban
context, aynı tur tavanı; ölçü = API girdi token'ı. Cevaplar tohum başına bir taze kör hakemle puanlanır.
claude -p sonnet (abonelik, ücretli API yok). Çıktı: .claude/beyin2/kosu2/<adım>.json + sonuc.txt
"""
import json
import random
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).parent
KOK = D.parent.parent
CIKTI = D / "kosu2"
PROJ = Path.home() / ".claude/projects/C--Projeler-omer-skills"
CL = shutil.which("claude")
TUR = "8"
BEYIN_KOMUT = "python tools/beyin.py ara"

CEVAP_A = """Aşağıdaki soruları cevapla. Tek bilgi kaynağın ikinci beyin araması (Bash'te yalnız bu komut):
python tools/beyin.py ara "<soru>"
(birebir kaynak satırları + yol:satır döner; çıktı bütçelidir, eksik kalırsa soruyu farklı anahtar kelimelerle yinele ya da --k 5). Başka komut (grep, cat, dosya okuma) çalıştırma.
Tur az olsun: ilk turda tüm soruların aramalarını TEK mesajda paralel Bash çağrılarıyla yap; ikinci turda yalnız
eksik kalanlar için sorguyu farklı kelimelerle yinele; sonra cevapla. Arka plan komutu kullanma.
Çıktı: YALNIZ JSONL, soru başına bir satır: {"id":…,"cevap":"kısa cevap","kaynak":"yol:satır"}
Sorular:
"""

CEVAP_B = """Aşağıdaki soruları cevapla. Tek aracın Read (Grep/Glob/Bash yok). Bilgi kaynağın C:\\Projeler\\omer-skills
deposundaki dosyalar (.kos/kopru/, docs/, tools/), C:\\Projeler\\omer-kurallar.md, ~/.claude/CLAUDE.md ve
~/.claude/projects/C--Projeler-omer-skills/memory/. Tur az olsun: ilk turda tüm okumaları TEK mesajda paralel yap.
Çıktı: YALNIZ JSONL, soru başına bir satır: {"id":…,"cevap":"kısa cevap","kaynak":"yol:satır"}
Sorular:
"""

HAKEM = """Bağımsız değerlendiricisin. Her satırda soru, referans cevap ve aday cevap var. Aday cevap referanstaki ana olguyu
doğru veriyorsa 1 (eş anlamlı ifade ve fazladan doğru bilgi kabul), ana olgu eksik/yanlışsa 0. "cok": true sorularda
referanstaki iki parçanın ikisi de gerekli. Araç kullanma.
Çıktı: YALNIZ JSONL: {"id":…,"d":0|1,"neden":"≤10 kelime"}
"""


def cagir(ad, istem, arac=None, izin=None, tur=None):
    argv = [CL, "-p", "--model", "sonnet", "--output-format", "json",
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    if arac:  # --allowedTools kısıtlamaz (global izinler grep'e açık); araç kümesini --tools belirler
        argv += ["--tools", arac]
    if izin:
        argv += ["--allowedTools", izin]
    if tur:
        argv += ["--max-turns", tur]
    r = subprocess.run(argv, input=istem, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=KOK, timeout=3600, creationflags=0x08000000)
    (CIKTI / f"{ad}.json").write_text(r.stdout or r.stderr, encoding="utf-8")
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {"result": "", "hata": (r.stderr or r.stdout)[:300]}


def mesajlar(d, dizin):
    t = Path(dizin) / f"{d.get('session_id')}.jsonl"
    if d.get("session_id") and t.exists():
        for x in t.read_text(encoding="utf-8").splitlines():
            m = json.loads(x).get("message") or {}
            if m.get("role") == "assistant" and isinstance(m.get("content"), list):
                yield from m["content"]


def satirlar(d, dizin=PROJ):
    """result yalnız son mesajdır; JSONL cevapları önceki mesajlarda kalabilir → tüm transkript + result, son gelen id kazanır."""
    metin = "\n".join(c.get("text", "") for c in mesajlar(d, dizin) if c.get("type") == "text")
    out = {}
    for s in (metin + "\n" + (d.get("result") or "")).splitlines():
        s = s.strip().strip("`")
        if s.startswith("{"):
            try:
                j = json.loads(s)
            except ValueError:
                continue
            out[j.get("id", len(out))] = j
    return list(out.values())


def ihlal(d, dizin=PROJ):
    """A kolunda beyin.py ara dışındaki Bash komutlarının sayısı."""
    return sum(1 for c in mesajlar(d, dizin) if c.get("type") == "tool_use" and c.get("name") == "Bash"
               and not c.get("input", {}).get("command", "").strip().startswith(BEYIN_KOMUT))


def girdi(d):
    return sum(u.get("inputTokens", 0) + u.get("cacheReadInputTokens", 0) + u.get("cacheCreationInputTokens", 0)
               for u in (d.get("modelUsage") or {}).values())


def main():
    CIKTI.mkdir(exist_ok=True)
    qs = [json.loads(s) for s in (D / "sorular.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    cok = [q for q in qs if q.get("cok")]
    tek = [q for q in qs if not q.get("cok")]
    r = random.Random(2005)  # d1 ile aynı bölme
    r.shuffle(cok)
    r.shuffle(tek)
    setler = {2005: cok[:10] + tek[:10], 2006: cok[10:20] + tek[10:20]}
    for t, s in setler.items():
        random.Random(t).shuffle(s)

    def liste(s):
        return "\n".join(f'{q["id"]}. {q["soru"]}' for q in s)
    isler = {f"A{t}": (CEVAP_A + liste(s), "Bash", f"Bash({BEYIN_KOMUT}:*)", TUR) for t, s in setler.items()}
    isler["B2005"] = (CEVAP_B + liste(setler[2005]), "Read", None, TUR)
    ad = sys.argv[1:] or list(isler)
    with ThreadPoolExecutor(3) as ex:
        sonuc = dict(zip(ad, ex.map(lambda k: cagir(k, *isler[k]), ad)))

    def hakem(t):
        cev = {c.get("id"): c.get("cevap") for c in satirlar(sonuc[f"A{t}"])}
        satir = [json.dumps({"id": q["id"], "soru": q["soru"], "referans": q["cevap"], "cok": q.get("cok", False),
                             "aday": cev.get(q["id"], "")}, ensure_ascii=False) for q in setler[t]]
        return satirlar(cagir(f"hakem{t}", HAKEM + "\n".join(satir)))
    if "B2005" not in sonuc and (CIKTI / "B2005.json").exists():  # B değişmedi: önceki koşu yeniden kullanılır
        sonuc["B2005"] = json.loads((CIKTI / "B2005.json").read_text(encoding="utf-8"))
    hs = [t for t in setler if f"A{t}" in sonuc]
    with ThreadPoolExecutor(2) as ex:
        puan = dict(zip(hs, ex.map(hakem, hs)))
    rapor = []
    for t in hs:
        d = {p.get("id"): p.get("d", 0) for p in puan[t]}
        s = setler[t]
        a = sonuc[f"A{t}"]
        rapor.append(f"tohum {t}: {sum(d.get(q['id'], 0) for q in s)}/{len(s)}"
                     f" (çok-notlu {sum(d.get(q['id'], 0) for q in s if q.get('cok'))}/{sum(bool(q.get('cok')) for q in s)})"
                     f" · A girdi {girdi(a)} tur {a.get('num_turns')} ihlal {ihlal(a)} · yanlış {[q['id'] for q in s if not d.get(q['id'])]}")
    if "A2005" in sonuc and "B2005" in sonuc:
        a, b = girdi(sonuc["A2005"]), girdi(sonuc["B2005"])
        rapor.append(f"token 2005: A {a} ↔ B {b} (tur {sonuc['B2005'].get('num_turns')}) = %{100 * a // max(b, 1)}")
    (CIKTI / "sonuc.txt").write_text("\n".join(rapor) + "\n", encoding="utf-8")
    print("\n".join(rapor))


if __name__ == "__main__":
    main()
