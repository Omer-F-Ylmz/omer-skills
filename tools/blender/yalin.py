"""BLENDER-1: tarif işini yalın claude -p oturumunda koşturur — MCP/skill/hook/CLAUDE.md öneki yok (~80k → ~5k jeton/tur).

    python tools/blender/yalin.py "<istek>" [--blend <dosya.blend>] [--tek]

Sistem istemi = tarif.py docstring'i + geçerli ışık/malzeme adları + 3 adımlık iş akışı; araçlar yalnız Write + Bash.
--tek (BLENDER-2): model araçsız tek yanıtta spec JSON verir, yalin Blender'ı kendisi koşar; hata/eksikte 1 düzeltme turu
(tur başına önek yeniden okunmaz: 4–7 tur → 1–2).
Çıktı: son mesaj + jeton/tur/usd özeti (JSON).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools" / "blender" / "lib"))
import tarif  # noqa: E402

CLI, TARIF = KOK / "tools" / "blender_cli.py", KOK / "tools" / "blender" / "lib" / "tarif.py"


TEK_AKIS = ("Araç yok: yanıtın YALNIZ tek ```json bloğunda spec olsun (yollar mutlak); spec'i sistem koşar, sonucu sana döner. "
            "İstenen her çıktıyı tek spec'e koy: nesneler/duzenle, isik, kamera (oto ya da {konum, hedef, lens}), kaydet, glb, "
            "onizle {yol, px, motor: eevee}, render, ozet. İstekte ölçüsü verilen her nesne için \"beklenen\": {ad: [x, y, z]} "
            "(m, dış kutu; çap 8 cm silindir → [0.08, 0.08, …]) ekle — sistem ölçülen kutuyla ±%15 karşılaştırır. "
            "Hata dönerse yalnız düzeltilmiş spec'i ver.\n")


def sistem(tek=False):
    profiller, tarifler = tarif._ad_listesi()
    return (f"Blender sahne işini tek spec JSON ile yaparsın; bpy kodu yazmazsın.\n{tarif.__doc__}\n"
            f"Işık profilleri: {profiller}\nMalzeme tarifleri: {tarifler}\n"
            + (TEK_AKIS if tek else
               "İş akışı (en çok 4 tur):\n"
            "1) Write ile spec.json yaz (istenen klasöre; yollar mutlak). İstenen her çıktıyı tek spec'e koy: nesneler/duzenle, "
            "isik, kamera (oto ya da {konum, hedef, lens}), kaydet, glb, onizle {yol, px, motor: eevee}, render, ozet.\n"
            f"2) Bash: python \"{CLI}\" \"{TARIF}\" @<spec.json> [--blend <başlangıç.blend>]\n"
            "3) SONUC JSON'unda gecti ve ozet'i istekle karşılaştır; hata/eksik varsa spec'i bir kez düzeltip yeniden koş.\n"
            "4) Kısa sonuç yaz (istenen sayılar dahil). Başka dosya okuma, keşif yapma.\n")
            + "Kalite: ürün tanınır biçimde olsun (koni+ust ile gövde, ekler ile sap/ağız/tutamak); gerçekçi ölçü (m); "
            "ışık profili malzemeye uygun (sırlı seramik: seramik_sirli, metal: metal).")


def bayraklar():
    return ["--setting-sources", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
            "--tools", "Write,Bash", "--allowedTools", "Write", "Bash", "--system-prompt", sistem()]


def tek_bayraklar():
    return ["--setting-sources", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
            "--tools", "", "--system-prompt", sistem(tek=True)]


def _claude(istek, ek):
    r = subprocess.run(["claude", "-p", istek, "--model", "sonnet", "--output-format", "json", *ek],
                       capture_output=True, text=True, encoding="utf-8", timeout=1500)
    j = json.loads(r.stdout or "{}")
    return {"metin": j.get("result") or "", "usage": j.get("usage") or {}, "tur": j.get("num_turns") or 0,
            "usd": j.get("total_cost_usd") or 0.0, "rc": r.returncode}


def tek(istek, blend=None, kos=_claude, calistir=None, hafif=True):
    """Araçsız tek tur + yerel koşu; hata/eksikte (dogrula ya da Blender) en çok 1 düzeltme turu. kosucu.kos biçiminde dict döner.
    hafif=False: 1.2.0 tabanı (biçim düzeltmesi yok; faz5 'tek' kolu)."""
    if calistir is None:
        sys.path.insert(0, str(KOK / "tools"))
        from blender_cli import calistir
    t = {"usage": {}, "tur": 0, "usd": 0.0, "sure": 0.0, "araclar": [], "rc": 1, "hata": ""}
    istem, spec, hata, bek = istek, None, [], {}
    for i in range(2):
        o = kos(istem, tek_bayraklar())
        for k, v in (o.get("usage") or {}).items():
            if isinstance(v, (int, float)):
                t["usage"][k] = t["usage"].get(k, 0) + v
        t["tur"] += o.get("tur") or 0
        t["usd"] += o.get("usd") or 0.0
        t["sure"] += o.get("sure") or 0.0
        m = re.search(r"\{.*\}", o.get("metin") or "", re.S)
        try:
            spec = json.loads(m.group(0))
            bek = spec.pop("beklenen", None) or {}  # ölçü kapısı: dogrula/Blender görmez, ozet'le karşılaştırılır
            if bek:
                spec["ozet"] = list(dict.fromkeys([*spec.get("ozet", []), "ad", "boyut"]))
            t.setdefault("ilk_spec", json.loads(json.dumps(spec)))  # BLENDER-4 d2: duzelt öncesi ilk tur (faz5 tek4K)
            hata = tarif.dogrula(tarif.duzelt(spec) if hafif else spec)
        except (AttributeError, ValueError) as e:
            spec, hata = None, [f"spec JSON ayrıştırılamadı: {e}"]
        if not hata:
            kod, sonuc, _ = calistir(TARIF, spec, blend)
            if kod == 0:
                olcu = {o.get("ad"): o.get("boyut") for o in sonuc.get("ozet") or [] if isinstance(o, dict)}
                hata = [f"ölçü sapması {ad}: beklenen {b}, ölçülen {olcu.get(ad)} (±%15; ekler gövdeye birleşir, dış kutuyu büyütür)"
                        for ad, b in bek.items()
                        if not olcu.get(ad) or any(abs(x - y) > 0.15 * y for x, y in zip(olcu[ad], b))]
                if not hata or i:
                    return {**t, "rc": 0, "ilk_hata": t.get("ilk_hata", ""), "spec": spec, "metin": json.dumps(sonuc, ensure_ascii=False), "hata": "; ".join(hata)[-200:]}
            else:
                hata = [f"blender_cli exit {kod}: {json.dumps(sonuc, ensure_ascii=False)[:1500]}"]
        t.setdefault("ilk_hata", str(hata)[-300:])  # BLENDER-3: düzeltme turunun nedeni (ölçümde ek tur KALITE'den mi?)
        istem = (f"{istek}\n\nÖnceki spec:\n{json.dumps({**(spec or {}), **({'beklenen': bek} if bek else {})}, ensure_ascii=False)}"
                 f"\nHata: {hata}\nDüzeltilmiş spec'i ver.")
    return {**t, "metin": f"HATA: {hata}", "hata": str(hata)[-200:]}


def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    istek = a[0] + (f"\nBaşlangıç sahnesi: --blend {a[a.index('--blend') + 1]}" if "--blend" in a else "")
    if "--tek" in a:
        o = tek(a[0], a[a.index("--blend") + 1] if "--blend" in a else None)
        print(json.dumps({"sonuc": o["metin"], "tur": o["tur"], "usd": o["usd"], "usage": o["usage"]}, ensure_ascii=False))
        return o["rc"]
    o = _claude(istek, bayraklar())
    print(json.dumps({"sonuc": o["metin"], "tur": o["tur"], "usd": o["usd"], "usage": o["usage"]}, ensure_ascii=False))
    return 0 if o["rc"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
