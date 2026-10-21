"""ORDU-1 d11 A/B: aynı iki gerçek (salt okuma) iş, A = eski soyut önsöz, B = yeni somut tetikli önsöz. claude -p toplam 4 (tavan 6).
Çıktı: .claude/ordu3/d11_ab.json (iş × kol: tur, USD, Agent/ucuz_alt sayısı, yanıt). Kullanım: arka.py ile koş."""
import json, re, subprocess, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / ".kos/kopru"))
sys.path.insert(0, str(KOK / "tools/olcum"))
import ajan_sira
from ordu_onsoz_tara import DIZIN

ESKI = ("ORDU-1 derleyici: işi böl; keşif/okuma/özet/test koşusunu alt ajana ver. Kademe: "
        "`python tools/ordu.py sinif \"<iş>\"` (kolay=ücretsiz, orta=iki ücretsiz aile/Haiku, zor=Sonnet, imkansiz=Opus). "
        "Sen yalnız derle, doğrula, iyileştir.\n\n")
IS = {
    "okuma": "tools/ucuz_alt.py, tools/ordu.py, .kos/kopru/ajan_sira.py ve onay/ordu_1.py dosyalarını incele; ORDU bayrağının açılma/kapanma akışını "
             "ve her dosyanın rolünü ≤8 satırda özetle. Hiçbir dosyayı değiştirme.",
    "test": "tests/test_ajan_sira.py, tests/test_ordu.py ve tests/test_ordu_olc.py testlerini koş (rtk python -m pytest); geçen/kalan sayısını ve "
            "kırmızı test adlarını ≤5 satırda ver. Hiçbir dosyayı değiştirme.",
}


def kos(onek, istem):
    argv, env = ajan_sira.baslat_argv("high", "sonnet")
    p = subprocess.run(argv, input=(onek + istem + "\n\n[bütçe] En fazla 25 tur kullan.").encode("utf-8"), cwd=str(KOK), env=env,
                       capture_output=True, creationflags=0x08000000, timeout=1500)
    return json.loads(p.stdout.decode("utf-8", "replace"))


def say(sid):
    """Araç sayıları; ucuz_alt yalnız Bash'te `python .../ucuz_alt.py` çağrısı (dosyayı Read/Grep etmek sayılmaz)."""
    ar = {}
    for s in (DIZIN / f"{sid}.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            o = json.loads(s)
        except ValueError:
            continue
        c = (o.get("message") or {}).get("content")
        if o.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if b.get("type") == "tool_use":
                    k = "ucuz_alt" if b["name"] == "Bash" and re.search(r"python\S* \S*ucuz_alt\.py", b["input"].get("command", "")) else b["name"]
                    ar[k] = ar.get(k, 0) + 1
    return ar


sonuc = []
for ad, istem in IS.items():
    for kol, onek in (("A", ESKI), ("B", ajan_sira.ORDU_ONEK)):
        j = kos(onek, istem)
        sonuc.append({"is": ad, "kol": kol, "tur": j.get("num_turns"), "usd": j.get("total_cost_usd"),
                      "araclar": say(j["session_id"]), "yanit": j.get("result")})
        (KOK / ".claude/ordu3/d11_ab.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
