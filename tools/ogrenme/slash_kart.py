"""SLASH-ÖĞREN d5 madde 1: TDD kartı eşli ölçüm (2 `claude -p`: skill'li / skill'siz). Kırmızı test, kaynak düzeltmesinden önce görüldü mü + tur + maliyet.
Sonuç .kos/ogrenme/slash-kart.json. Kullanım: python slash_kart.py <boş_çalışma_dizini>"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KAYNAK = "import re\n\n\ndef slugify(s):\n    return re.sub(r'[^a-z0-9]', '-', s.lower())\n"
GOREV = "slug.py içindeki slugify('Hello  World') 'hello--world' döndürüyor, 'hello-world' olmalı (ardışık ayraçlar tek tire, uçlarda tire yok). Düzelt. Yalnız bu dizinde çalış, kısa bitir."
ONEK = "Önce Skill aracıyla test-driven-development skill'ini çağır ve onu izle. "


def kos(dizin, istem):
    dizin.mkdir(parents=True, exist_ok=True)
    (dizin / "slug.py").write_text(KAYNAK, encoding="utf-8")
    p = subprocess.run([shutil.which("claude"), "-p", "--output-format", "stream-json", "--verbose", "--model", "sonnet", "--max-turns", "14",
                        "--permission-mode", "acceptEdits", "--allowedTools", "Bash(python:*) Bash(pytest:*) Bash(py:*) Bash(rtk:*)"],
                       input=istem, capture_output=True, text=True, encoding="utf-8", cwd=str(dizin), timeout=600)
    (dizin / "ham.jsonl").write_text(p.stdout, encoding="utf-8")
    olay = [json.loads(s) for s in p.stdout.splitlines() if s.startswith("{")]
    arac, kirmizi, kaynak_duz, skill = [], None, None, False
    sonuclar = {}
    for o in olay:
        m = o.get("message")
        for b in (m.get("content") if isinstance(m, dict) else None) or []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use":
                ad, g = b["name"], b.get("input") or {}
                arac.append(ad)
                skill = skill or ad == "Skill"
                hedef = Path(g.get("file_path", "")).name
                if ad in ("Edit", "Write") and hedef == "slug.py" and kaynak_duz is None:
                    kaynak_duz = len(arac)
                if ad == "Bash" and ("pytest" in g.get("command", "") or "unittest" in g.get("command", "")):
                    sonuclar[b["id"]] = len(arac)
            elif b.get("type") == "tool_result" and b.get("tool_use_id") in sonuclar and kirmizi is None:
                c = json.dumps(b.get("content"))
                if "failed" in c.lower() or "FAIL" in c or "AssertionError" in c:
                    kirmizi = sonuclar[b["tool_use_id"]]
    son = next((o for o in reversed(olay) if o.get("type") == "result"), {})
    u = son.get("usage") or {}
    return {"skill_cagrildi": skill, "arac_sirasi": arac, "kirmizi_adim": kirmizi, "kaynak_duzeltme_adim": kaynak_duz,
            "kirmizi_once": kirmizi is not None and (kaynak_duz is None or kirmizi < kaynak_duz),
            "tur": son.get("num_turns"), "maliyet_usd": son.get("total_cost_usd"),
            "girdi_toplam": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0),
            "cikti": u.get("output_tokens")}


if __name__ == "__main__":
    kok = Path(sys.argv[1])
    sonuc = {"skillsiz": kos(kok / "B", GOREV), "skilli": kos(kok / "A", ONEK + GOREV)}
    (KOK / ".kos" / "ogrenme" / "slash-kart.json").write_text(json.dumps(sonuc, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(sonuc, ensure_ascii=False))
