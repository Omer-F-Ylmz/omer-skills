"""BLENDER-1: tarif işini yalın claude -p oturumunda koşturur — MCP/skill/hook/CLAUDE.md öneki yok (~80k → ~5k jeton/tur).

    python tools/blender/yalin.py "<istek>" [--blend <dosya.blend>]

Sistem istemi = tarif.py docstring'i + geçerli ışık/malzeme adları + 3 adımlık iş akışı; araçlar yalnız Write + Bash.
Çıktı: son mesaj + jeton/tur/usd özeti (JSON).
"""
import json
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools" / "blender" / "lib"))
import tarif  # noqa: E402

CLI, TARIF = KOK / "tools" / "blender_cli.py", KOK / "tools" / "blender" / "lib" / "tarif.py"


def sistem():
    profiller, tarifler = tarif._ad_listesi()
    return (f"Blender sahne işini tek spec JSON ile yaparsın; bpy kodu yazmazsın.\n{tarif.__doc__}\n"
            f"Işık profilleri: {profiller}\nMalzeme tarifleri: {tarifler}\n"
            "İş akışı (en çok 4 tur):\n"
            "1) Write ile spec.json yaz (istenen klasöre; yollar mutlak). İstenen her çıktıyı tek spec'e koy: nesneler/duzenle, "
            "isik, kamera (oto ya da {konum, hedef, lens}), kaydet, glb, onizle {yol, px, motor: eevee}, render, ozet.\n"
            f"2) Bash: python \"{CLI}\" \"{TARIF}\" @<spec.json> [--blend <başlangıç.blend>]\n"
            "3) SONUC JSON'unda gecti ve ozet'i istekle karşılaştır; hata/eksik varsa spec'i bir kez düzeltip yeniden koş.\n"
            "4) Kısa sonuç yaz (istenen sayılar dahil). Başka dosya okuma, keşif yapma.\n"
            "Kalite: ürün tanınır biçimde olsun (koni+ust ile gövde, ekler ile sap/ağız/tutamak); gerçekçi ölçü (m); "
            "ışık profili malzemeye uygun (sırlı seramik: seramik_sirli, metal: metal).")


def bayraklar():
    return ["--setting-sources", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
            "--tools", "Write,Bash", "--allowedTools", "Write", "Bash", "--system-prompt", sistem()]


def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    istek = a[0] + (f"\nBaşlangıç sahnesi: --blend {a[a.index('--blend') + 1]}" if "--blend" in a else "")
    r = subprocess.run(["claude", "-p", istek, "--model", "sonnet", "--output-format", "json", *bayraklar()],
                       capture_output=True, text=True, encoding="utf-8", timeout=1500)
    j = json.loads(r.stdout or "{}")
    print(json.dumps({"sonuc": j.get("result"), "tur": j.get("num_turns"), "usd": j.get("total_cost_usd"),
                      "usage": j.get("usage")}, ensure_ascii=False))
    return 0 if r.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
