"""ZORUNLU-ARAÇ-1 (Ömer 22 Eki): öğrenilen araçları görevde ZORUNLU kılar. ajan_sira.py kullanır.
blok(ad, metin): ön uçuş → katalog_ara en uygun 8 skill/ajan/cli + `beyin ara` 3 ders + ruflo hata-dersi → isteme "ZORUNLU ARAÇLAR" bloğu; liste <ad>.zorunlu.json.
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


def araclar(metin):
    """katalog_ara en uygun N kayıt; ajan-sira oturumunda boş MCP (--strict-mcp-config) olduğundan mcp elenir."""
    sys.path.insert(0, str(KOK / "tools"))
    try:
        import katalog_ara
        q = metin[:600]
        sonuc = katalog_ara.suz(katalog_ara.aday(q, N + 6), katalog_ara.yigin(q))[0]
    except Exception:
        return []
    return [{"ad": o["ad"], "tur": o["tur"], "cagri": o["cagri"], "ne": (o["is"] or o["metin"])[:90]}
            for o in sonuc if o["tur"] != "mcp" and "reposunda" not in o["metin"]][:N]


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


def blok(ad, metin):
    ar = araclar(metin)
    if not ar:
        return ""
    ders = _calistir([sys.executable, "-I", str(KOK / "tools/beyin.py"), "ara", metin[:300], "--k", "3", "--butce", "450"], 40)
    hata = ruflo_ders(metin)
    (SIRA / f"{ad}.zorunlu.json").write_text(json.dumps({"araclar": ar, "gorsel": bool(GORSEL.search(metin))}, ensure_ascii=False), encoding="utf-8")
    s = ["ZORUNLU ARAÇLAR (bitişte oturum dökümünden sayılır; ≥%d kullanılmazsa görev arac_eksik işaretlenir ve yeniden kuyruğa girer):" % min(3, math.ceil(len(ar) / 2))]
    s += [f"- {o['ad']} ({o['tur']}) · {o['ne']} · çağrı: {o['cagri'][:60]}" for o in ar]
    if GORSEL.search(metin):
        s.append("- gorsel_hakem (görsel iş: `python .kos/kopru/gorsel_hakem.py` çağrısı olmadan kanit_eksik)")
    if ders:
        s.append("Beyin dersleri:\n" + ders[:900])
    if hata:
        s.append("Hata-dersi (ruflo): " + hata)
    return "\n".join(s) + "\n\n"


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
        return any(s == ad or s.endswith(":" + ad) for s in sk)
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


def denetle(ad):
    """<ad>.json + <ad>.zorunlu.json → <ad>.denetim.json ({durum, eksik}); liste ya da döküm yoksa None."""
    try:
        z = json.loads((SIRA / f"{ad}.zorunlu.json").read_text(encoding="utf-8"))
        sid = json.loads((SIRA / f"{ad}.json").read_text(encoding="utf-8")).get("session_id")
    except (OSError, ValueError):
        return None
    k = _kullanimlar(sid) if sid else None
    if k is None:
        return None
    durum, yok = karar(z["araclar"], z["gorsel"], k)
    d = {"durum": durum, "eksik": yok}
    (SIRA / f"{ad}.denetim.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def yeniden_istem(ad, istem, eksik):
    """Eksik araçlarla yeniden kuyruk için görev dosyası (KOK'a göreli yol döner)."""
    yol = GOREV / f"{ad}-a.md"
    yol.write_text((KOK / istem).read_text(encoding="utf-8") + f"\n\nkullanmadığın araçlar: {', '.join(eksik)} — bu turda bunları kullan.\n", encoding="utf-8")
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
    print("ad\tliste\tkullanılan\tdurum")
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
        print(f"{p.stem}\t{len(ar)}\t{len(ar) - len(yok)}\t{durum}")
    print(f"toplam {say} · işaretlenen {eksik}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 2 and sys.argv[1] == "--geri":
        geri(int(sys.argv[2]))
