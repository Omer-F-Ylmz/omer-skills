"""ÖĞREN-1 A6 kalite kapısı: aynı köprü işi (TOKEN-3 k11) araclar'lı (güncel profil) ↔ araclar'sız (token4-yedek).
Kol başına 1 claude -p; transkriptten ilk istek girdi token'ı + çağrılan araçlar + araç hatası.
  python -X utf8 .claude/ogren1/kapi_a6.py"""
import json, re, subprocess, sys, tempfile, time
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / ".kos/kopru"))
sys.path.insert(0, str(KOK / ".claude/token3"))
import ajan_sira, cc_profil  # noqa: E402

D = Path(__file__).parent
ISTEM = ("Mekanik iş, yorum yok. 1) `python -m pytest tests/test_ajan_sira.py tests/test_cc_profil.py -q` koş. "
         "2) .kos/kopru/ajan-sira.tsv boş olmayan satır sayısını say. Yanıt tam 2 satır: `pytest: <passed sayısı> passed, <failed> failed` ve `tsv: <n>`.")
# d15: kalan 2 köprü işi farklı araç yolları (Grep/Glob, git); `kapi_a6.py araclar k12` — yer gerçeği betik dışında sayılır
ISTEMLER = {"k11": ISTEM,
            "k12": "Mekanik iş, yorum yok. Grep aracıyla skills/departman-verimlilik/SKILL.md içinde `rtk` geçen satır sayısını, "
                   "Glob aracıyla .claude/ogren1/*.py dosya sayısını bul. Yanıt tam 2 satır: `grep: <n>` ve `glob: <n>`.",
            "k13": "Mekanik iş, yorum yok. `git log -1 --format=%h -- docs/ogren/token.md` koş; docs/ogren/token.md satır sayısını say. "
                   "Yanıt tam 2 satır: `commit: <hash>` ve `satir: <n>`."}
TABAN =ajan_sira.ARGV[:ajan_sira.ARGV.index('{"mcpServers":{}}') + 1]
yedek = cc_profil.kur("ajan", profiller=KOK / "profiller/cc-arka.json.token4-yedek",
                      gecici=Path(tempfile.gettempdir()) / "cc_profil_yedek")[0]
KOLLAR = {"araclar": ajan_sira.ARGV, "yedek": [*TABAN, *yedek]}


def transkript(sid):
    t = next(Path.home().glob(f".claude/projects/*/{sid}.jsonl"), None)
    ilk, araclar, hata = None, [], []
    for s in (t.read_text(encoding="utf-8").splitlines() if t else []):
        m = json.loads(s).get("message") or {}
        u = m.get("usage")
        if u and ilk is None:
            ilk = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        for c in m.get("content") or [] if isinstance(m.get("content"), list) else []:
            if c.get("type") == "tool_use":
                araclar.append(c["name"])
            if c.get("type") == "tool_result" and re.search(r"No such tool|not available|unknown tool", str(c.get("content")), re.I):
                hata.append(str(c.get("content"))[:120])
    return ilk, araclar, hata


is_ = sys.argv[2] if len(sys.argv) > 2 else "k11"
for ad in sys.argv[1:2] or KOLLAR:
    t = time.time()
    p = subprocess.run(KOLLAR[ad], input=ISTEMLER[is_], capture_output=True, text=True, encoding="utf-8", cwd=KOK,
                       env={k: v for k, v in __import__("os").environ.items() if k != "CLAUDE_CODE_EFFORT_LEVEL"}, timeout=1200)
    (D / f"kapi-{ad}{'' if is_ == 'k11' else '-' + is_}.json").write_text(p.stdout or p.stderr, encoding="utf-8")
    j = json.loads(p.stdout) if p.stdout.strip().startswith("{") else {}
    ilk, araclar, hata = transkript(j.get("session_id", "-"))
    print(ad, "rc", p.returncode, f"{time.time() - t:.0f}s", "ilk_girdi", ilk, "tur", j.get("num_turns"),
          "araclar", ",".join(araclar), "hata", hata, "sonuc", (j.get("result") or "").replace("\n", " | ")[:160], flush=True)
