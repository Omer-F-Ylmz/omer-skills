"""GRAPHIFY-ULTRA-1 G4: Read PreToolUse kancası (köprü ajanı profili, profiller/cc-arka.json).
>300 satırlık dosyanın offset/limit'siz ilk Read'i reddedilir, gerekçede regex iskeleti (sembol · satır) döner;
aynı oturumda aynı dosya ikinci kez istenirse geçer (kaçış yolu). Graf yüklenmez: her zaman taze, ~50 ms.
Sınama: python tools/oku_yonlendir.py --sina"""
import json, os, re, sys, tempfile
from pathlib import Path

ESIK, TAVAN = 300, 40
ATLA = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".ipynb", ".svg"}
DESEN = re.compile(
    r"^\s*(?:async\s+)?(?:def|class)\s+\w+"                                    # py
    r"|^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function\*?|class)\s+\w+"  # js/ts
    r"|^\s*(?:export\s+)?const\s+\w+\s*=\s*(?:async\s*)?(?:\(|function|\w+\s*=>)"
    r"|^\s*\w+\.registerTool\(\s*\""
    r"|^\s*(?:public|private|protected|internal)\s[^=;]*\("                    # cs
    r"|^\s*(?:public\s+|internal\s+)?(?:sealed\s+|static\s+|abstract\s+|partial\s+)*(?:class|interface|record|enum)\s+\w+"
    r"|^#{1,3} \S")                                                            # md


def iskelet(satirlar):
    s = [(i + 1, x.strip()[:90]) for i, x in enumerate(satirlar) if DESEN.match(x)]
    if len(s) > TAVAN:  # önce üst düzey (girintisiz) semboller
        s = [(n, x) for n, x in s if not satirlar[n - 1][:1].isspace()] or s
    ek = f"\n… +{len(s) - TAVAN} sembol" if len(s) > TAVAN else ""
    return "\n".join(f"L{n}\t{x}" for n, x in s[:TAVAN]) + ek


def karar(g, durum_dizin):
    t = g.get("tool_input") or {}
    yol = t.get("file_path") or ""
    if t.get("offset") or t.get("limit") or t.get("pages") or Path(yol).suffix.lower() in ATLA:
        return None
    try:
        satirlar = Path(yol).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    if len(satirlar) <= ESIK:
        return None
    kayit = Path(durum_dizin) / f"{re.sub(r'[^\w-]', '_', g.get('session_id') or 'yok')}.txt"
    gorulen = kayit.read_text(encoding="utf-8").splitlines() if kayit.exists() else []
    if yol in gorulen:
        return None
    kayit.parent.mkdir(parents=True, exist_ok=True)
    with kayit.open("a", encoding="utf-8") as f:
        f.write(yol + "\n")
    return (f"{len(satirlar)} satır — tam okuma yerine iskelet (sembol · satır). Gereken kısmı Read offset/limit ile "
            f"aç; konum için Grep -n. Tam dosya gerçekten gerekiyorsa aynı Read'i tekrarla (ikincisi geçer).\n"
            + (iskelet(satirlar) or "(sembol bulunamadı — Grep -n ile konum bul)"))


def main():
    g = json.load(sys.stdin)
    neden = karar(g, Path(tempfile.gettempdir()) / "oku_yonlendir")
    if neden:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": neden}}, ensure_ascii=False))


def sina():
    with tempfile.TemporaryDirectory() as d:
        uzun = Path(d) / "a.py"
        uzun.write_text("".join(f"def f{i}():\n    pass\n" if i % 10 == 0 else "x = 1\n" for i in range(400)), encoding="utf-8")
        kisa = Path(d) / "b.py"
        kisa.write_text("x = 1\n" * 10, encoding="utf-8")
        g = {"session_id": "s1", "tool_input": {"file_path": str(uzun)}}
        n = karar(g, d)
        assert n and "L1\tdef f0():" in n and "440 satır" in n, n
        assert karar(g, d) is None                                   # ikinci istek geçer
        assert karar({**g, "session_id": "s2", "tool_input": {"file_path": str(uzun), "offset": 5}}, d) is None
        assert karar({"session_id": "s3", "tool_input": {"file_path": str(kisa)}}, d) is None
        assert iskelet(["# Baş", "  def ic():", "class A:"]) == "L1\t# Baş\nL2\tdef ic():\nL3\tclass A:"
    print("oku_yonlendir sina: 5/5")


if __name__ == "__main__":
    sina() if "--sina" in sys.argv else main()
