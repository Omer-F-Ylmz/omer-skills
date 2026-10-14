"""ENVANTER-4 d2 m2a: deterministik kartlardan (kilavuz_derin kart) OmniRoute ücretsiz combo ile derin alan taslağı.

python tools/kilavuz_taslak.py 2-4,7,9-69   → .kos/kopru/envanter4/cikti/pNNN-t.jsonl + docs/katalog/derin-jeton.tsv
Ücretli model yok (combo ucretsiz-ozet2: gemini flash-lite → OpenRouter :free); karar/doğrulama Claude'da (kilavuz_ornek.py).
Sınıflandırıcı engelli güvenlik aileleri modele gönderilmez, "katalog" işaretiyle yazılır (Desktop kararı 2).
"""
import json, os, re, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kilavuz_derin as kd

# d4: gemini-önlü combo'lar asılı kalıyor (1 kelimelik istem 90 sn zaman aşımı) → işçi başına TASLAK_COMBO ile ücretsiz model
URL, COMBO = "http://127.0.0.1:20128/v1/chat/completions", os.environ.get("TASLAK_COMBO", "ucretsiz-ozet2")
ENGELLI = {"mukul975", "davila7"}  # d1: Agent sınıflandırıcısına takılan güvenlik aileleri
GRUP = 8
JETON = kd.KAT / "derin-jeton.tsv"
ISTEM = """Aşağıda Claude Code yetenek kartları var (skill / ajan / plugin / mcp / cli). Her kart için TEK SATIR JSON yaz; başka metin, kod çiti, açıklama YAZMA:
{"ad":"<kart başlığındaki ad, aynen>","nasil":"...","neden":"...","en_iyi":"...","birlikte":"...","tuzak":"...","maliyet":"..."}
Alanlar Türkçe, her biri en çok 120 karakter, tek cümle:
- nasil: nasıl çalışır — kartın başlıklarından/gövdesinden somut adımlar ya da komut ("X komutuyla çağrılır" tek başına YETMEZ)
- neden: hangi iş/durumda seçilir
- en_iyi: en iyi sonuç için pratik ipucu
- birlikte: kartta adı geçen, birlikte kullanılan araç/skill/ajan; yoksa "?"
- tuzak: kartta görülen sınır, risk ya da yaygın hata
- maliyet: jeton/süre/bağımlılık yükü (gövde boyu, ağır komut, gereken anahtar ADI)
KURAL: Yalnız karttaki metne dayan. Kartta olmayan komut, bayrak, sürüm, sayı, araç adı, örnek UYDURMA; kartta bilgi yoksa o alana yalnız "?" yaz.
Genel/yuvarlak ifade YASAK ("verimliliği artırır", "en iyi uygulamaları izleyin", "dikkatli kullanın" gibi) — her alan bu karta özgü somut bilgi ya da "?". Anahtar/sır değeri yazma.

"""


def env_oku(ad):
    if os.environ.get(ad):
        return os.environ[ad]
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, ad)[0]
    except OSError:
        return None


def bloklar(metin):
    """kart → [(ad, tur, aile, blok)]"""
    out = []
    for b in re.split(r"(?m)^(?=## )", metin):
        m = re.match(r"## (.+)\ntür (\S+) · aile (\S+)", b)
        if m:
            out.append((m.group(1).strip(), m.group(2), m.group(3), b.strip()))
    return out


def ayikla(yanit, beklenen):
    """Model yanıtından geçerli satırlar; ad beklenenlerden biri, tüm alanlar dolu str."""
    out, y, i, dec = {}, yanit or "", 0, json.JSONDecoder()
    while (i := y.find("{", i)) != -1:
        try:
            j, i = dec.raw_decode(y, i)
        except ValueError:
            i += 1
            continue
        if isinstance(j, dict) and j.get("ad") in beklenen and all(isinstance(j.get(a), str) and j[a].strip() for a in kd.ALAN):
            out[j["ad"]] = {"ad": j["ad"], **{a: j[a].strip() for a in kd.ALAN}}
    return out


def iste(istem, anahtar):
    q = urllib.request.Request(URL, method="POST", data=json.dumps({
        "model": COMBO, "messages": [{"role": "user", "content": istem}], "max_tokens": 6000, "reasoning_effort": "low",
        "temperature": 0.2}).encode(), headers={"content-type": "application/json", "authorization": f"Bearer {anahtar}",
                                                "user-agent": "envanter4-taslak/1"})  # Python-urllib UA Groq'ta 403
    for bekle in (0, 20, 60, 120):
        time.sleep(bekle)
        try:
            j = json.load(urllib.request.urlopen(q, timeout=180))
            return j["choices"][0]["message"]["content"] or "", j.get("model", "?"), j.get("usage") or {}, ""
        except Exception as e:  # anahtar hata metnine girmez
            hata = f"{type(e).__name__} {getattr(e, 'code', '')}".strip()
    return "", "-", {}, hata


def parti(no, anahtar):
    kart = kd.IS / "kart" / f"p{no:03d}.md"
    cikti = kd.IS / "cikti" / f"p{no:03d}-t.jsonl"
    derin = kd.KAT / "derin.jsonl"
    var = {f"{j.get('tur')}:{j['ad']}" for j in map(json.loads, open(derin, encoding="utf8"))} if derin.exists() else set()
    if cikti.exists():
        var |= {f"{j.get('tur')}:{j['ad']}" for j in map(json.loads, open(cikti, encoding="utf8"))}
    kalan = [b for b in bloklar(kart.read_text(encoding="utf8")) if f"{b[1]}:{b[0]}" not in var]
    say = {"cagri": 0, "giris": 0, "cikis": 0, "yaz": 0, "katalog": 0, "eksik": 0, "model": set(), "hata": set()}
    t0 = time.time()
    with open(cikti, "a", encoding="utf8", newline="\n") as f:
        for ad, tur, aile, _ in [b for b in kalan if b[2] in ENGELLI]:
            f.write(json.dumps({"ad": ad, "tur": tur, "durum": "katalog"}, ensure_ascii=False) + "\n")
            say["katalog"] += 1
        acik = [b for b in kalan if b[2] not in ENGELLI]
        kuyruk = [acik[i:i + GRUP] for i in range(0, len(acik), GRUP)]
        while kuyruk:
            g = kuyruk.pop(0)
            yanit, model, u, hata = iste(ISTEM + "\n\n".join(b[3] for b in g), anahtar)
            say["cagri"] += 1
            say["giris"] += u.get("prompt_tokens", 0)
            say["cikis"] += u.get("completion_tokens", 0)
            say["model"].add(model)
            if hata:
                say["hata"].add(hata)
            bulunan = ayikla(yanit, {b[0] for b in g})
            for ad, tur, _, _ in g:
                if ad in bulunan:
                    f.write(json.dumps({**bulunan[ad], "tur": tur}, ensure_ascii=False) + "\n")
                    say["yaz"] += 1
            eksik = [b for b in g if b[0] not in bulunan]
            if eksik and len(g) > 1:  # eksikler tek tek bir kez daha
                kuyruk += [[b] for b in eksik]
            elif eksik:
                say["eksik"] += 1
            f.flush()
    sat = [f"p{no:03d}", say["cagri"], say["giris"], say["cikis"], say["yaz"], say["katalog"], say["eksik"],
           int(time.time() - t0), "/".join(sorted(say["model"])), "/".join(sorted(say["hata"])) or "-"]
    yeni = not JETON.exists()
    with open(JETON, "a", encoding="utf8", newline="\n") as f:
        if yeni:
            f.write("parti\tcagri\tgiris_jeton\tcikis_jeton\tyazilan\tkatalog\teksik\tsn\tmodel\thata\n")
        f.write("\t".join(map(str, sat)) + "\n")
    print(*sat, sep="\t", flush=True)


def araliklar(s):
    return [n for p in s.split(",") for n in (range(int(p.split("-")[0]), int(p.split("-")[-1]) + 1))]


assert araliklar("2-4,7") == [2, 3, 4, 7]
assert list(ayikla('x {"ad":"a","nasil":"n","neden":"n","en_iyi":"e","birlikte":"?","tuzak":"t","maliyet":"m"} {"ad":"z"}', {"a"})) == ["a"]
assert [b[:3] for b in bloklar("## a\ntür skill · aile x · çağrı\nk\n\n## b\ntür ajan · aile y · ç\n")] == [("a", "skill", "x"), ("b", "ajan", "y")]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    anahtar = env_oku("OMNIROUTE_KEY")
    if not anahtar:
        sys.exit("OMNIROUTE_KEY yok")
    for no in araliklar(sys.argv[1]):
        parti(no, anahtar)
