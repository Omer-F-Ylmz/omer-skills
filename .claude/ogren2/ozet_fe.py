"""ÖĞREN-2 frontend-tasarım özet hattı: ÖĞREN-1 ozet3 kol A (ne_yapar · komut · girdi_cikti · sinirlar + birebir alıntı doğrulaması)
aynı şema ve kollarla; kaynak listesi katalog-son.jsonl (kategori_son=frontend-tasarım, kurulu, kanonik). Mekanizma (kol B) token'a özgü → sorulmaz.
Ayar/MCP .json kaynakları dış modele GÖNDERİLMEZ (env/anahtar sızıntısı) → Claude elle kartlar.
  python -X utf8 .claude/ogren2/ozet_fe.py [id ...]   ·   python -X utf8 .claude/ogren2/ozet_fe.py --sina"""
import json, sys, time, zipfile
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / ".claude/ogren1"))
import ozet3  # noqa: E402

KAT = KOK / ".kos/kopru/ogren/katalog-son.jsonl"
CIKTI = KOK / ".kos/kopru/ogren/ozet-frontend.jsonl"
ozet3.TAVAN = 900  # yalnız :free/yerel kollar; 569 kalem × ~1.5 çağrı
# 20 Eki: nemotron-3-super :free OpenRouter'da 404, gemma 429 → ultra başa
ozet3.KOL_A = [("omni", "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free")] + ozet3.KOL_A


def kalemler():
    r = [json.loads(s) for s in KAT.read_text(encoding="utf-8").splitlines()]
    return {x["id"]: x for x in r if x.get("kategori_son") == "frontend-tasarım" and x["tur"] not in ("aday", "model")
            and x.get("kanonik") == x["id"] and x.get("yol") and not x["yol"].lower().endswith(".json")}


def metin(yol):
    if "!" in yol:  # zip!iç/yol
        z, ic = yol.split("!", 1)
        with zipfile.ZipFile(z) as f:
            return f.read(ic).decode("utf-8", "replace")
    y = Path(yol)
    if y.is_dir():
        y = next((y / n for n in ("SKILL.md", "README.md", "readme.md") if (y / n).is_file()), None) \
            or next(y.rglob("SKILL.md"), None) or next(y.rglob("plugin.json"))
    return y.read_text(encoding="utf-8", errors="replace")


if __name__ == "__main__":
    K = kalemler()
    if sys.argv[1:] == ["--sina"]:
        assert not any(x["yol"].lower().endswith(".json") for x in K.values()), "ayar .json dış modele gidiyor"
        assert "frontend" in metin(K["k02453"]["yol"]).lower() and metin(K["k03390"]["yol"])
        z = next(x for x in KAT.read_text(encoding="utf-8").splitlines() if '.zip!' in x)
        assert metin(json.loads(z)["yol"])
        print("sina ✓", len(K))
        sys.exit()
    bitti = {json.loads(s)["id"] for s in CIKTI.read_text(encoding="utf-8").splitlines()} if CIKTI.exists() else set()
    for i in sys.argv[1:] or sorted(K, key=lambda i: "ABC-".index(K[i]["katman"] or "-")):
        x = K[i]
        if i in bitti:
            continue
        try:
            m = metin(x["yol"])
        except Exception as e:
            print(i, x["ad"], "KAYNAK-YOK", type(e).__name__, flush=True)
            continue
        t, g = time.time(), ozet3.bolumlu(m)
        a, ma = ozet3.kos(ozet3.KOL_A, ozet3.SEMA_A, x["ad"], m, g,
                          lambda o, m: ozet3.gecerli_a(o, m, ozet3.adlari(x["ad"], x["yol"])))
        if not a:
            print(i, x["ad"], "KOLLAR-RET", flush=True)
            continue
        a.update(id=i, ad=x["ad"], tur=x["tur"], katman=x["katman"], kaynak=x["yol"], model=ma, etiket=ozet3.ETIKET, sn=round(time.time() - t))
        with CIKTI.open("a", encoding="utf-8") as f:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
        print(i, x["ad"], ma, "ok", flush=True)
    print("BITTI cagri", ozet3.CAGRI, flush=True)
