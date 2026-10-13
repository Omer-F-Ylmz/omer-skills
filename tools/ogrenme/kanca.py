"""RUFLO-1 d9: günlük öğrenme döngüsü — CC kancası (SubagentStart · SubagentStop · SessionEnd), ölçüm dışındaki gerçek oturumlar için.
  SubagentStart: ana transkriptten alt ajanın istemini bulur → ders.getir (≤1, kısa biçim, alaka eşiği; yalnız kod ailesi) → additionalContext.
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
ESIK, TEST_ODUL, PAY = 5.0, 0, 0.0  # d12 kalibre.py: Jev Opus etiketiyle ters (ort. 2.2 başarı / 3.6 başarısız); hiçbir yargıç Opus'un 5 başarısızını ayırmadı → orta nokta
YARGIC_MODEL = "sonnet"  # Opus başarılılarını tanıma: sonnet 46/55, haiku 32/55 (d10 hatası: başarılı koşudan 'kaçın' dersi)
SORU = {"kalite": {"type": "score", "criteria": ["Hiç karşılamıyor / alakasız", "Çok zayıf", "Kısmen, önemli eksik",
                                                 "Çoğunlukla, küçük eksik", "Tam karşılıyor", "Tam ve örnek nitelikte"],
                   "instructions": "`yanit`, `gorev` isteğini ne kadar doğru ve eksiksiz karşılıyor? Biçim/uzunluk değil, içerik."}}
ETIKET = ("Aşağıda Claude Code alt ajan koşuları var (görev, araç/hata sayısı, son test sonucu, son araç çıktıları, son mesaj, "
          "çalışma klasörünün kural belgeleri ve son teslim dosyasının şimdiki hâli). "
          "Her koşu için: ajan görevi GERÇEKTEN başardı mı (istenen iş yapıldı, doğrulandı ya da doğrulanamadığı dürüstçe bildirildi "
          "ve iş yine de doğru)? Kural belgesi varsa teslim dosyası her kurala (biçim, başlık, sıra, birim vb.) uymalı; bir kural "
          "ihlali ya da teslim yokluğu başarısızlıktır — son mesajın iddiasına değil teslim dosyasına bak. "
          "basari 1/0, guven 0-1. Yalnız JSON liste: [{\"no\": n, \"basari\": 0|1, \"guven\": x}]\n\n%s")
KURAL_BELGE = ("KURALLAR.md", "CLAUDE.md", "AGENTS.md")
# d17 KABUL yalnız kod ailesinde (d13 kod seti 1.0, jeton ×0.40): istem kod/test dosyası anmıyorsa ders yok; OGRENME_KANCA=hepsi ölçüm içindir
KOD_AILESI = re.compile(r"\.(py|js|ts|tsx|cs|go|rs|java|rb|php)\b|\btest", re.I)
DAMIT = ("Aşağıda bir Claude Code oturumundaki alt ajan koşuları ve yargıç puanları var. Gelecekteki BENZER görevlerde işe yarayacak "
         "EN FAZLA 3 genellenebilir ders çıkar (kural/yöntem; göreve özgü sayı, dosya içeriği, yol, ad değil). BAŞARILI koşudan "
         "'işe yarayan yöntem' dersi (asla 'kaçın' değil); BAŞARISIZ koşudan 'kaçın' dersi (hatanın kaynağı + ilk turda ne yapılmalı). "
         "Koşu bir proje kural belgesine (KURALLAR.md, CLAUDE.md vb.) uyduysa ya da onu kaçırdıysa dersi o somut kurala bağla. "
         "Tur azaltan dersleri öne al (bağımsız okumaları paralel yap, "
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


def _test_sonucu(cikti, hata):
    """Test komutu çıktısı → 1 geçti · 0 kırmızı · None (izin reddi/belirsiz)."""
    if re.search(r"denied|izin|approval|onay gerek", cikti, re.I):
        return None
    if re.search(r"\bfail|\berror\b|Traceback", cikti, re.I):
        return 0
    if re.search(r"\bpassed\b|^OK\b", cikti, re.M):
        return 0 if hata else 1
    return 0 if hata else None


def baglam(cwd, teslim, sinir=1500):
    """d14: yargıç kural belgesini görmüyordu (kalibre zor gerçek başarısızlık 0/8) → cwd kural belgeleri + son teslim dosyasının şimdiki hâli."""
    yollar = [Path(cwd) / a for a in KURAL_BELGE] if cwd else []
    parca = [f"--- {y.name}\n{y.read_text(encoding='utf-8', errors='replace')[:sinir]}" for y in yollar if y.is_file()]
    t = Path(cwd or ".", teslim) if teslim else None
    parca.append(f"--- teslim {teslim}\n{t.read_text(encoding='utf-8', errors='replace')[:sinir]}" if t and t.is_file()
                 else "--- teslim: yok (Edit/Write yok)")
    return "\n".join(parca)


def yorunge(transkript):
    """Alt ajan transkriptinden → (görev, araç sayısı, hata sayısı, tur, son metin, son test sonucu 1/0/None, baglam)."""
    gorev, arac, hata, tur, son, test, testler, cwd, teslim = "", 0, 0, 0, "", None, set(), None, None
    for x in _satirlar(transkript):
        cwd = cwd or x.get("cwd")
        for p in _icerik(x):
            if x.get("type") == "user" and p.get("type") == "text" and not gorev:
                gorev = p.get("text", "")
            elif p.get("type") == "tool_use":
                arac += 1
                if p.get("name") in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
                    teslim = (p.get("input") or {}).get("file_path") or (p.get("input") or {}).get("notebook_path") or teslim
                if re.search(r"pytest|unittest|\btest", str((p.get("input") or {}).get("command", ""))):
                    testler.add(p.get("id"))
            elif p.get("type") == "tool_result":
                hata += bool(p.get("is_error"))
                if p.get("tool_use_id") in testler:
                    c = p.get("content")
                    c = c if isinstance(c, str) else " ".join(y.get("text", "") for y in c or [] if isinstance(y, dict))
                    t = _test_sonucu(c, p.get("is_error"))
                    test = test if t is None else t
            elif x.get("type") == "assistant" and p.get("type") == "text" and p.get("text", "").strip():
                son = p["text"]
        tur += x.get("type") == "assistant"
    return gorev, arac, hata, tur, son, test, baglam(cwd, teslim)


def _ekle(oturum, kayit):
    with open(kuyruk(oturum), "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")


def kanca(girdi, baslat=None):
    """→ stdout'a yazılacak metin ('' = yok). baslat(oturum): arka plan isle (testte sahte)."""
    olay, oturum, ajan = girdi.get("hook_event_name"), girdi.get("session_id", ""), girdi.get("agent_type") or ""
    if olay == "SubagentStart" and ajan and girdi.get("transcript_path"):
        istem = istem_bul(girdi["transcript_path"], ajan)
        if os.environ.get("OGRENME_KANCA") != "hepsi" and not KOD_AILESI.search(istem):
            return ""
        blok, ids = ders.getir(ajan, istem, k=1, kosu=oturum[:8], kisa=True)
        if not blok:
            return ""
        _ekle(oturum, {"tip": "getir", "ajan_id": girdi.get("agent_id"), "ajan": ajan, "ids": ids})
        return json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": blok}}, ensure_ascii=False)
    if olay == "SubagentStop" and ajan and girdi.get("agent_transcript_path"):
        gorev, arac, hata, tur, son, test, bag = yorunge(girdi["agent_transcript_path"])
        _ekle(oturum, {"tip": "bitti", "ajan_id": girdi.get("agent_id"), "ajan": ajan, "gorev": gorev[:2000], "arac": arac,
                       "hata": hata, "tur": tur, "test": test, "son": (girdi.get("last_assistant_message") or son)[-3000:], "baglam": bag,
                       "ciktilar": son_ciktilar(girdi["agent_transcript_path"])})
    elif olay == "SessionEnd" and kuyruk(oturum).exists():
        (baslat or _arka)(oturum)
    return ""


def _arka(oturum):
    import subprocess
    subprocess.run([sys.executable, str(ARKA), str(ders.dizin() / "kanca.log"), str(Path(__file__).resolve()), "isle", oturum],
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5,
                   creationflags=0x08000000)  # CREATE_NO_WINDOW; arka.py kendisi ayrık süreç açıp hemen döner


def karma(jev, arac, hata, son, test=None, odul=None):
    """Jev 0-10 + nesnel işaret: araç hata oranı ve boş sonuç düşürür; son test geçti/kırmızı ± TEST_ODUL (Jev metne bakar, yörüngeyi görmez)."""
    if not son.strip():
        return 0.0
    odul = TEST_ODUL if odul is None else odul
    return round(min(10.0, max(0.0, jev - 4 * hata / max(arac, 1) + odul * ((test == 1) - (test == 0)))), 1)


def guvenli(k):
    """Ders yazma/geri bildirim kapısı: karma eşiğe PAY'dan yakınsa yargı belirsiz → dokunma."""
    return k is not None and abs(k - ESIK) >= PAY


def isle(oturum, yargic=None, damit=None):
    """Oturum başı ≤1 yargı çağrısı + ≤1 damıtma çağrısı. → işlenen yörünge sayısı (atlandıysa 0)."""
    yol = kuyruk(oturum)
    kayit = list(_satirlar(yol)) if yol.exists() else []
    bitti = [k for k in kayit if k["tip"] == "bitti"][-5:]
    if not bitti:
        return 0
    try:
        puan = (yargic or _yargic)(bitti)
    except Exception as h:  # ağ/anahtar/tavan: sessiz geç, kuyruk atlandı olarak kalır
        print(time.strftime("%H:%M:%S"), oturum[:8], "yargı atlandı:", type(h).__name__, flush=True)
        yol.rename(yol.with_suffix(".atlandi"))
        return 0
    for k, j in zip(bitti, puan):
        k["karma"] = None if j is None else karma(j, k["arac"], k["hata"], k["son"], k.get("test"))
    getirilen = {k["ajan_id"]: k["ids"] for k in kayit if k["tip"] == "getir"}
    for k in bitti:
        if guvenli(k["karma"]) and getirilen.get(k["ajan_id"]):
            ders.geri_bildir(getirilen[k["ajan_id"]], k["karma"] >= ESIK)
    ogretici = sorted((k for k in bitti if guvenli(k["karma"]) and k["arac"] >= EN_AZ_ARAC),
                      key=lambda k: abs(k["karma"] - ESIK), reverse=True)[:EN_FAZLA_YORUNGE]
    yeni = 0
    if ogretici:
        metin = "\n\n".join(f"Koşu {i}: ajan {k['ajan']} · {'BAŞARILI' if k['karma'] >= ESIK else 'BAŞARISIZ'} (puan {k['karma']}/10) · "
                            f"{k['tur']} tur · {k['arac']} araç · {k['hata']} hata · son test {k.get('test')}\n"
                            f"Görev: {k['gorev'][:800]}\nSon mesaj: {k['son'][-800:]}\n{k.get('baglam') or ''}" for i, k in enumerate(ogretici, 1))
        try:
            m = (damit or _damit)(DAMIT % metin)
            for x in json.loads(m[m.index("["):m.rindex("]") + 1])[:ders.EN_FAZLA_ADAY]:
                k = ogretici[int(x.get("no", 1)) - 1]
                ders.ekle(k["ajan"], str(x["baslik"]), str(x["kosul"]), str(x["icerik"]), "basari" if k["karma"] >= ESIK else "basarisizlik",
                          f"oturum-{oturum[:8]}", f"karma {k['karma']}", k["gorev"][:200])
                yeni += 1
        except (ValueError, KeyError, TypeError, IndexError) as h:  # sırlı ders ValueError ile reddedilir
            print(time.strftime("%H:%M:%S"), oturum[:8], "damıtma:", h, flush=True)
    print(time.strftime("%H:%M:%S"), oturum[:8], f"yargı {len(bitti)} · karma {[k['karma'] for k in bitti]} · ders {yeni}", flush=True)
    yol.rename(yol.with_suffix(".islendi"))
    return len(bitti)


def _jev(states, tasiyici=None):
    """tasiyici: jev Tasiyici sözleşmesi (yargila(states, questions) → [{q: {score 0-5, confidence}}]); LAYA-1 adayı buraya takılır."""
    sys.path.insert(0, str(KOK / "tools" / "olcum"))
    sys.path.insert(0, str(KOK / "tools" / "jev"))
    from jev.cekirdek import Tasiyici
    from jev_yargic import yargila
    cevap = yargila(states, SORU, tasiyici or Tasiyici(en_fazla=1, istek_tavan=10), ag_bekle=())  # kanca: ≤5 yörünge → ≤5 istek
    return [None if c is None else c["kalite"]["score"] * 2 for c in cevap]


def son_ciktilar(yol, n=3):
    c = []
    for x in _satirlar(yol, 512_000):
        for p in _icerik(x):
            if p.get("type") == "tool_result":
                t = p.get("content")
                c.append(t if isinstance(t, str) else " ".join(y.get("text", "") for y in t or [] if isinstance(y, dict)))
    return [t[-300:] for t in c[-n:]]


def etiket_metni(kayitlar):
    return "\n\n".join(f"Koşu {i}: {k['arac']} araç · {k['hata']} hata · test {k.get('test')}\nGörev: {k['gorev'][:500]}\n"
                       f"Son çıktılar: {' | '.join(t[-200:] for t in k.get('ciktilar') or [])}\n"
                       f"Son mesaj: {(k.get('son') or k.get('yanit') or '')[-500:]}\n{k.get('baglam') or ''}" for i, k in enumerate(kayitlar, 1))


def _yargic(kayitlar, model=None):
    """Varsayılan yargıç (d12): Jev puanı Opus etiketleriyle ilişkisiz çıktı (kalibre.py) → Opus etiket istemiyle haiku, ≤1 çağrı.
    → koşu başına 0-10 = 5 ± 5·güven (başarı +, başarısızlık −); okunamayan koşu None."""
    m = _damit(ETIKET % etiket_metni(kayitlar), model or YARGIC_MODEL)
    e = {int(x["no"]): x for x in json.loads(m[m.index("["):m.rindex("]") + 1])}
    return [round(5 + 5 * float(e[i].get("guven") or 0) * (1 if e[i].get("basari") else -1), 1) if i in e else None
            for i in range(1, len(kayitlar) + 1)]


def _damit(istem, model="haiku"):
    sys.path.insert(0, str(KOK / "tools" / "olcum"))
    os.environ.pop("ANTHROPIC_API_KEY", None)  # Ömer 12 Eki: API kredisi kapalı, plan limiti
    os.environ["OGRENME_KANCA"] = "0"  # damıtma oturumu kendi kancasını tetiklemez
    import kosucu
    o = kosucu.kos(istem, ek=["--strict-mcp-config", "--max-turns", "1"], model=model, butce=0.2 if model == "haiku" else 0.6, timeout=180)
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
