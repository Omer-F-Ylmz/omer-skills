"""RUFLO-1 d9: günlük öğrenme döngüsü — CC kancası (SubagentStart · SubagentStop · SessionEnd), ölçüm dışındaki gerçek oturumlar için.
  SubagentStart: ana transkriptten alt ajanın istemini bulur → ders.getir (≤2, alaka eşiği) → additionalContext.
  SubagentStop:  alt ajan yörüngesini (görev · araç/hata sayısı · son mesaj) oturum kuyruğuna yazar (ağ yok).
  SessionEnd:    kuyrukta biten alt ajan varsa `isle` arka planda (.kos/kopru/arka.py, pencere yok); kanca hemen döner.
  python kanca.py isle <oturum>: 1 Jev çağrısı (önbellekli) + karma yargı → geri_bildir → ≤1 haiku damıtma → ≤3 ders.
Kanca her hatayı yutar (rc 0, çıktı yok); OGRENME_KANCA=0 kapatır. Ağ/anahtar yoksa isle sessizce atlar."""
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ders  # noqa: E402

KOK = Path("C:/Projeler/omer-skills")
ARKA = KOK / ".kos" / "kopru" / "arka.py"
EN_FAZLA_YORUNGE, EN_AZ_ARAC = 3, 3  # damıtmaya en fazla 3 yörünge; <3 araçlık koşu öğretmez (jeton tavanı)
SORU = {"kalite": {"type": "score", "criteria": ["Hiç karşılamıyor / alakasız", "Çok zayıf", "Kısmen, önemli eksik",
                                                 "Çoğunlukla, küçük eksik", "Tam karşılıyor", "Tam ve örnek nitelikte"],
                   "instructions": "`yanit`, `gorev` isteğini ne kadar doğru ve eksiksiz karşılıyor? Biçim/uzunluk değil, içerik."}}
DAMIT = ("Aşağıda bir Claude Code oturumundaki alt ajan koşuları ve yargıç puanları var. Gelecekteki BENZER görevlerde işe yarayacak "
         "EN FAZLA 3 genellenebilir ders çıkar (kural/yöntem; göreve özgü sayı, dosya içeriği, yol, ad değil). Düşük puanlı koşudan "
         "'kaçın' dersi (hatanın kaynağı + ilk turda ne yapılmalı); tur azaltan dersleri öne al (bağımsız okumaları paralel yap, "
         "gereksiz doğrulama turu yok). icerik tek cümle ≤25 kelime, örneksiz. Öğretici bir şey yoksa [] döndür. Yalnız JSON liste: "
         '[{"no": koşu no, "baslik": "kural", "kosul": "ne zaman uygulanır", "icerik": "ne yapılmalı"}]\n\n%s')


def kuyruk(oturum):
    d = ders.dizin() / "kuyruk"
    d.mkdir(exist_ok=True)
    return d / f"{re.sub(r'[^\w-]', '', oturum)[:64] or 'yok'}.jsonl"


def _satirlar(yol, kuyruk_bayt=None):
    with open(yol, "rb") as f:
        if kuyruk_bayt:
            f.seek(max(0, f.seek(0, 2) - kuyruk_bayt))
        for s in f.read().decode("utf-8", "replace").splitlines():
            try:
                yield json.loads(s)
            except ValueError:
                continue


def _icerik(x):
    m = x.get("message") or {}
    c = m.get("content")
    return [{"type": "text", "text": c}] if isinstance(c, str) else (c or [])


def _ad(s):
    return re.sub(r"[\s_-]", "", (s or "").lower())


def istem_bul(transkript, ajan):
    """Ana transkriptin sonundaki Agent/Task çağrılarından bu ajan türüne ait son istem (yoksa "")."""
    son = ""
    for x in _satirlar(transkript, 512_000):
        for p in _icerik(x):
            g = p.get("input") or {}
            if p.get("type") == "tool_use" and p.get("name") in ("Agent", "Task") and _ad(g.get("subagent_type")) == _ad(ajan):
                son = f"{g.get('description', '')}\n{g.get('prompt', '')}"
    return son


def yorunge(transkript):
    """Alt ajan transkriptinden → (görev, araç sayısı, hata sayısı, tur, son metin)."""
    gorev, arac, hata, tur, son = "", 0, 0, 0, ""
    for x in _satirlar(transkript):
        for p in _icerik(x):
            if x.get("type") == "user" and p.get("type") == "text" and not gorev:
                gorev = p.get("text", "")
            elif p.get("type") == "tool_use":
                arac += 1
            elif p.get("type") == "tool_result" and p.get("is_error"):
                hata += 1
            elif x.get("type") == "assistant" and p.get("type") == "text" and p.get("text", "").strip():
                son = p["text"]
        tur += x.get("type") == "assistant"
    return gorev, arac, hata, tur, son


def _ekle(oturum, kayit):
    with open(kuyruk(oturum), "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")


def kanca(girdi, baslat=None):
    """→ stdout'a yazılacak metin ('' = yok). baslat(oturum): arka plan isle (testte sahte)."""
    olay, oturum, ajan = girdi.get("hook_event_name"), girdi.get("session_id", ""), girdi.get("agent_type") or ""
    if olay == "SubagentStart" and ajan and girdi.get("transcript_path"):
        blok, ids = ders.getir(ajan, istem_bul(girdi["transcript_path"], ajan), kosu=oturum[:8])
        if not blok:
            return ""
        _ekle(oturum, {"tip": "getir", "ajan_id": girdi.get("agent_id"), "ajan": ajan, "ids": ids})
        return json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": blok}}, ensure_ascii=False)
    if olay == "SubagentStop" and ajan and girdi.get("agent_transcript_path"):
        gorev, arac, hata, tur, son = yorunge(girdi["agent_transcript_path"])
        _ekle(oturum, {"tip": "bitti", "ajan_id": girdi.get("agent_id"), "ajan": ajan, "gorev": gorev[:2000], "arac": arac,
                       "hata": hata, "tur": tur, "son": (girdi.get("last_assistant_message") or son)[-3000:]})
    elif olay == "SessionEnd" and kuyruk(oturum).exists():
        (baslat or _arka)(oturum)
    return ""


def _arka(oturum):
    import subprocess
    subprocess.run([sys.executable, str(ARKA), str(ders.dizin() / "kanca.log"), str(Path(__file__).resolve()), "isle", oturum],
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5,
                   creationflags=0x08000000)  # CREATE_NO_WINDOW; arka.py kendisi ayrık süreç açıp hemen döner


def karma(jev, arac, hata, son):
    """Jev 0-10 + nesnel işaret: araç hata oranı ve boş sonuç puanı düşürür (Jev metne bakar, yörüngeyi görmez)."""
    if not son.strip():
        return 0.0
    return round(max(0.0, jev - 4 * hata / max(arac, 1)), 1)


def isle(oturum, yargic=None, damit=None):
    """Oturum başı ≤1 yargı çağrısı + ≤1 damıtma çağrısı. → işlenen yörünge sayısı (atlandıysa 0)."""
    yol = kuyruk(oturum)
    kayit = list(_satirlar(yol)) if yol.exists() else []
    bitti = [k for k in kayit if k["tip"] == "bitti"][-5:]
    if not bitti:
        return 0
    try:
        puan = (yargic or _jev)([{"gorev": k["gorev"], "yanit": k["son"]} for k in bitti])
    except Exception as h:  # ağ/anahtar/tavan: sessiz geç, kuyruk atlandı olarak kalır
        print(time.strftime("%H:%M:%S"), oturum[:8], "yargı atlandı:", type(h).__name__, flush=True)
        yol.rename(yol.with_suffix(".atlandi"))
        return 0
    for k, j in zip(bitti, puan):
        k["karma"] = None if j is None else karma(j, k["arac"], k["hata"], k["son"])
    getirilen = {k["ajan_id"]: k["ids"] for k in kayit if k["tip"] == "getir"}
    for k in bitti:
        if k["karma"] is not None and getirilen.get(k["ajan_id"]):
            ders.geri_bildir(getirilen[k["ajan_id"]], k["karma"] >= 6)
    ogretici = sorted((k for k in bitti if k["karma"] is not None and k["arac"] >= EN_AZ_ARAC),
                      key=lambda k: abs(k["karma"] - 6), reverse=True)[:EN_FAZLA_YORUNGE]
    yeni = 0
    if ogretici:
        metin = "\n\n".join(f"Koşu {i}: ajan {k['ajan']} · puan {k['karma']}/10 · {k['tur']} tur · {k['arac']} araç · {k['hata']} hata\n"
                            f"Görev: {k['gorev'][:800]}\nSon mesaj: {k['son'][-800:]}" for i, k in enumerate(ogretici, 1))
        try:
            m = (damit or _damit)(DAMIT % metin)
            for x in json.loads(m[m.index("["):m.rindex("]") + 1])[:ders.EN_FAZLA_ADAY]:
                k = ogretici[int(x.get("no", 1)) - 1]
                ders.ekle(k["ajan"], str(x["baslik"]), str(x["kosul"]), str(x["icerik"]), "basari" if k["karma"] >= 6 else "basarisizlik",
                          f"oturum-{oturum[:8]}", f"karma {k['karma']}", k["gorev"][:200])
                yeni += 1
        except (ValueError, KeyError, TypeError, IndexError) as h:  # sırlı ders ValueError ile reddedilir
            print(time.strftime("%H:%M:%S"), oturum[:8], "damıtma:", h, flush=True)
    print(time.strftime("%H:%M:%S"), oturum[:8], f"yargı {len(bitti)} · karma {[k['karma'] for k in bitti]} · ders {yeni}", flush=True)
    yol.rename(yol.with_suffix(".islendi"))
    return len(bitti)


def _jev(states):
    sys.path.insert(0, str(KOK / "tools" / "olcum"))
    sys.path.insert(0, str(KOK / "tools" / "jev"))
    from jev.cekirdek import Tasiyici
    from jev_yargic import yargila
    cevap = yargila(states, SORU, Tasiyici(en_fazla=1, istek_tavan=10), ag_bekle=())  # en_fazla=1: oturum başı tek batch çağrı
    return [None if c is None else c["kalite"]["score"] * 2 for c in cevap]


def _damit(istem):
    sys.path.insert(0, str(KOK / "tools" / "olcum"))
    os.environ.pop("ANTHROPIC_API_KEY", None)  # Ömer 12 Eki: API kredisi kapalı, plan limiti
    os.environ["OGRENME_KANCA"] = "0"  # damıtma oturumu kendi kancasını tetiklemez
    import kosucu
    o = kosucu.kos(istem, ek=["--strict-mcp-config", "--max-turns", "1"], model="haiku", butce=0.2, timeout=180)
    return o["metin"]


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "isle":
        sys.stdout.reconfigure(encoding="utf-8")
        isle(sys.argv[2])
        return
    if os.environ.get("OGRENME_KANCA") == "0":
        return
    try:
        cikti = kanca(json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}"))
        if cikti:
            sys.stdout.buffer.write(cikti.encode("utf-8"))
    except Exception:  # kanca oturumu asla bozmaz
        pass


if __name__ == "__main__":
    main()
