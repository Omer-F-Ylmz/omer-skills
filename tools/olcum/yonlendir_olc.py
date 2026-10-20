"""ROUTER-1 d3 (20 Eki): d2 yapısı aynı; görev kademesi kural tablosundan (kod-oku/regex/alan-cikar T1), karışım son 7 gün köprü
iş kaydına göre (ogren 4 · video 3 · token 2 · atlas 1 · graphify+diğer 2), claude -p FORCE_PROMPT_CACHING_5M=1 (iki kolda).
ROUTER-1 d2 (20 Eki) ölçüm kapısı: 12 görev (3 T0 · 3 kolay · 3 orta · 3 zor), (A) Sonnet high ↔ (B) tools/yonlendir.py.
İki kol AYNI çağrı yapısı: T0 betik · T1 toplu · T2 toplu · T3 toplu, kart her toplu istemde. A'da T1–T3 Sonnet high; B'de T1
yonlendir.t1 zinciri (Groq → nemotron :free → ollama → Haiku), T2 Sonnet medium, T3 Sonnet high. T1 kalanı B'nin T2 topluna
katılır; T2 kalanı tek yükseltme çağrısıyla T3'e. claude -p ≤6 → T3 toplusu iki kolda birebir aynı çağrı (bir kez koşar, iki
kola yazılır) ve A bir kez koşar; B iki koşu. Kapı (her B koşusu): başarı ≥ A ve USD eşdeğeri ≥%30 az. Ücretsiz ≤60.
Kabul her görevde yerel ve mekanik (test/şema/eşitlik) — denetçi modeli yok. Ham yanıtlar <çıktı>/ altında.
  python .kos/kopru/arka.py <günlük> .kos/kopru/olcum_sira.py tools/olcum/yonlendir_olc.py <çıktı_dizini> [--yeniden]"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import model_sec  # noqa: E402
import ucuz_alt  # noqa: E402
import yonlendir  # noqa: E402

CAGRI_TAVAN, USD_TAVAN, UCRETSIZ_TAVAN = 6, 0.6, 60
KART = (KOK / "skills/is-akisi/references/calisma-karti.md").read_text(encoding="utf-8")
oku = lambda p, n=None: (KOK / p).read_text(encoding="utf-8")[:n]


def _tsv_toplam():
    s = [x.split("\t") for x in oku("docs/router-1/olcum.tsv").splitlines()]
    i, j = s[0].index("kol"), s[0].index("cikti")
    return sum(int(float(r[j])) for r in s[1:] if len(r) > j and r[i] == "A" and r[j].strip())


AJAN = {p.stem: re.search(r"^model:\s*(\S+)", p.read_text(encoding="utf-8"), re.M).group(1)
        for p in sorted((KOK / ".claude/agents").glob("*.md"))}
SKILL = sorted(p.name for p in (KOK / "skills").iterdir() if p.is_dir())
BIRLESIM = sorted(set(SKILL) | set(AJAN))
LIS = {"G04": ".claude/b2-olcum/.claude/skills/algorithmic-art/LICENSE.txt", "G05": ".claude/b2-olcum/.claude/skills/avoid-ai-writing/LICENSE.txt"}
COMMIT = "OMNİ-AYIR d2: json_al bozuk JSON yanıtında JSONDecodeError ile ölçümü düşürüyordu; kök neden çitli blok, düzeltildi + test"
ETIKET = ["hata-duzelt", "kod-yaz", "ozet-taslak", "lisans", "sayim"]
BUGLI = oku("tools/model_sec.py").split("if __name__")[0].replace("if i >= len(EFFORT):", "if i > len(EFFORT):")
assert BUGLI.count("if i > len(EFFORT):") == 1
REGEX_POZ = ["openrouter/nvidia/nemotron-3-super-120b-a12b:free", "openrouter/google/gemma-4-31b-it:free", "groq/llama-4:free"]
REGEX_NEG = ["cc-ucuz-free", "openrouter/x/y", "openrouter//y:free", "a/b:free:x", "openrouter/a b/c:free", ":free", "x:free"]
VRAPOR = oku("docs/video-tarama/2026-10-12-ig-DeV2n53gLgf.md")
KONU = ["model/llm", "site/frontend", "otomasyon/iş", "token", "3d/blender", "güvenlik", "oyun"]
VADAY = ["rea", "claude code", "codex", "notion", "electron", "skool"]


def _ozet3(y):
    s = str(y).strip().splitlines()
    return len(s) == 3 and all(x.startswith("- ") and len(x) <= 160 for x in s) and all(k in str(y) for k in ("REA", "Notion"))


def _kod_test(kod, test):
    """model kodu ayrı süreçte (-I, 20 sn) — asılı/zararlı kod ölçüm sürecini düşürmez"""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(f"{kod}\n\n{test}\nprint('TAMAM')\n")
    try:
        r = subprocess.run([sys.executable, "-I", f.name], capture_output=True, text=True, timeout=20, creationflags=0x08000000)
        return "TAMAM" in r.stdout
    except subprocess.TimeoutExpired:
        return False


JSON_TEST = r'''
assert json_al('{"a": 1}') == {"a": 1}
assert json_al('Sonuç:\n```json\n{"a": "x}y", "b": [1, 2]}\n```\nbitti') == {"a": "x}y", "b": [1, 2]}
assert json_al('önce {bozuk} sonra {"k": {"i": 2}} son') == {"k": {"i": 2}}
assert json_al('yok') is None and json_al('[1, 2]') is None and json_al('') is None
'''
SURE_TEST = r'''
for s, v in [("1:02:03", 3723), ("02:03", 123), ("1h2m3s", 3723), ("45s", 45), ("1.5m", 90), ("2h", 7200), (" 03:04 ", 184),
             ("0:00", 0), ("1m30s", 90), ("10:00:00", 36000)]:
    assert abs(sure_sn(s) - v) < 1e-9, (s, sure_sn(s))
for s in ["", "abc", "1:2:3:4", "5x", "h"]:
    try:
        sure_sn(s)
    except ValueError:
        continue
    raise AssertionError(s)
'''
HATA_TEST = f"import sys\nsys.path.insert(0, {str(KOK / 'tools')!r})\nimport model_sec as M\n" + "\n".join(
    f"assert bayraklar({a!r}, kademe={k}, arac={r!r}) == M.bayraklar({a!r}, kademe={k}, arac={r!r})"
    for a, k, r in [("yargi", 2, ()), ("mekanik", 0, ()), ("ajan", 3, ("Read", "Bash(git *)")), ("ozet", 5, ())])

# ad: (tür, seviye, istem, kabul(yanıt) → bool, T0 betiği | None)
GOREV = {
    "G01": ("sayim", "T0", "Bu TSV'de kol sütunu 'A' olan satırların cikti sütunu toplamı (boşlar 0). Yanıt: tamsayı.\n"
            + oku("docs/router-1/olcum.tsv"), lambda y: str(y).strip() == str(_tsv_toplam()), _tsv_toplam),
    "G03": ("birlestir", "T0", f"İki listenin birleşimi: tekil, Python sorted() sırasıyla JSON dizi.\nL1: {json.dumps(SKILL)}\n"
            f"L2: {json.dumps(sorted(AJAN))}", lambda y: y == BIRLESIM, lambda: BIRLESIM),
    "G05": ("lisans", "T1", "Bu lisans metninin SPDX kimliği nedir? Yanıt: SPDX dizgesi.\n" + oku(LIS["G05"], 1500),
            lambda y: str(y).strip().lower() == "mit", None),
    "G06": ("etiket", "T1", f"Bu commit iletisinin iş türü hangisi? Seçenekler: {' | '.join(ETIKET)}. Yanıt: seçeneklerden biri.\n{COMMIT}",
            lambda y: str(y).strip() == "hata-duzelt", None),
    "G07": ("kod-oku", "T1", "Aşağıdaki modülde bayraklar('yargi', kademe=2) dönüşündeki --model ve --effort değerleri? "
            "Yanıt: {\"model\": ..., \"effort\": ...}\n" + oku("tools/model_sec.py"),
            lambda y: isinstance(y, dict) and (y.get("model"), y.get("effort")) == tuple(
                model_sec.bayraklar("yargi", kademe=2)[i] for i in (1, 3)), None),
    "G08": ("regex", "T1", "OmniRoute ücretsiz model kimliğini re.fullmatch ile tanıyan Python regex yaz: '/' ile ayrılmış en az iki boş "
            "olmayan parça (sağlayıcı/…/model), boşluk yok, kimlik ':free' ile biter ve ':free' yalnız sonda; combo adları "
            "(cc-ucuz-free gibi) eşleşmez. Örnek: openrouter/google/gemma-4-31b-it:free ✓, openrouter/x/y ✗. Yanıt: regex dizgesi.",
            lambda y: _regex_ok(y), None),
    "G09": ("alan-cikar", "T1", "Bu betik belgesindeki çıkış kodlarını {\"kod\": \"anlam\"} JSON nesnesi olarak çıkar.\n"
            + "\n".join(oku("tools/ucuz_alt.py").splitlines()[:9]), lambda y: isinstance(y, dict) and set(y) == {"0", "1", "3", "4"}, None),
    "G10": ("kod-yaz", "T3", "Yalnız stdlib ile `def json_al(y: str) -> dict | None` yaz: model yanıtındaki İLK GEÇERLİ JSON NESNESİNİ "
            "döndür; ```json çiti, önde/arkada düzyazı, dizgi içinde { } ve önce bozuk {…} parçası olabilir; dizi nesne sayılmaz; "
            "yoksa None. Yanıt: tam Python kodu (dizge).", lambda y: _kod_test(str(y), JSON_TEST), None),
    "G11": ("hata-duzelt", "T3", "Bu modülde bayraklar('yargi', kademe=2) IndexError veriyor. Kök nedeni bul; düzeltilmiş TAM modülü "
            "(import'lar dahil, __main__ bloğu olmadan) ver. Yanıt: Python kodu (dizge).\n" + BUGLI,
            lambda y: _kod_test(str(y), HATA_TEST), None),
    "G13": ("etiket", "T1", f"Bu video raporunun konu etiketleri? Seçenekler: {' | '.join(KONU)}. Yanıt: 1–3 seçenekten JSON dizi.\n"
            + VRAPOR, lambda y: isinstance(y, list) and 1 <= len(y) <= 3 and "model/llm" in y and set(y) <= set(KONU), None),
    "G14": ("alan-cikar", "T1", "Bu video raporundaki aday araç/ürün adlarını JSON dizi olarak çıkar (yalnız özel adlar).\n" + VRAPOR,
            lambda y: isinstance(y, list) and sum(any(k == str(x).strip().lower() for x in y) for k in VADAY) >= 5, None),
    "G15": ("video-rapor", "T2", "Bu video raporunun Türkçe özeti: tam 3 satır, her satır '- ' ile başlar, ≤160 karakter, REA ve Notion "
            "adları geçer. Yanıt: 3 satırlık dizge.\n" + VRAPOR, _ozet3, None),
}
assert all(g[1] == yonlendir.sec(g[0])["kademe"] for g in GOREV.values())  # kademe kural tablosundan


def _regex_ok(y):
    try:
        r = re.compile(str(y))
    except re.error:
        return False
    return all(r.fullmatch(s) for s in REGEX_POZ) and not any(r.fullmatch(s) for s in REGEX_NEG)


def toplu_istem(adlar, kosu):
    """iki kolda aynı metin; koşu etiketi OmniRoute önbelleğini deler (koşu 2 gerçek çağrı olsun)"""
    g = "\n\n".join(f"## {a}\n{GOREV[a][2]}" for a in adlar)
    return f"{KART}\n[ROUTER-1 ölçüm koşu {kosu}]\n" + (
        f"Aşağıda {len(adlar)} bağımsız görev var. Araç kullanma. YALNIZ tek JSON nesnesi döndür; anahtarlar {', '.join(adlar)}, "
        f"değer her görevin istediği yanıt (kod yanıtları JSON dizgesi).\n\n{g}")


def json_ilk(y):
    i = (y or "").find("{")
    try:
        return json.JSONDecoder().raw_decode(y[i:])[0] if i >= 0 else None
    except ValueError:
        return None


class Sayac:
    claude = ucretsiz = 0


def claude(istem, kd, ham, yeniden):
    """(yanıt nesnesi, jeton, usd). stdin ile istem (argv'de uzun istem WinError 206); stderr ayrı (hook uyarıları JSON'u bozmaz)."""
    if not yeniden:
        if Sayac.claude >= CAGRI_TAVAN:
            raise RuntimeError("claude -p tavanı")
        Sayac.claude += 1
        r = subprocess.run(["claude", "-p", "--output-format", "json", "--max-budget-usd", str(USD_TAVAN), *yonlendir.argv(kd)],
                           input=istem, capture_output=True, text=True, encoding="utf-8", timeout=900, creationflags=0x08000000,
                           env={**os.environ, "FORCE_PROMPT_CACHING_5M": "1"})  # d3: tek atımlık çağrıda 1h yazımı ($4/M) yerine 5m ($2.5/M)
        ham.write_text(r.stdout, encoding="utf-8")
    try:
        d = json.JSONDecoder().raw_decode(ham.read_text(encoding="utf-8").lstrip())[0]
    except ValueError:  # boş/bozuk çıktı: görevler kalır, ham dosya incelemeye kalır
        return {}, 0, 0
    u = d.get("usage", {})
    jeton = sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
    return json_ilk(d.get("result", "")) or {}, jeton, d.get("total_cost_usd") or 0


def _sor(kol, model, g):
    if Sayac.ucretsiz >= UCRETSIZ_TAVAN:
        raise RuntimeError("ücretsiz tavanı")
    Sayac.ucretsiz += 1
    return ucuz_alt.sor(kol, model, g)


def _haiku(istem, mt):
    if Sayac.claude >= CAGRI_TAVAN:
        raise RuntimeError("claude -p tavanı")
    Sayac.claude += 1
    return yonlendir._haiku(istem, mt)


def _guvenli(f, y):
    try:
        return f(y)
    except Exception:
        return False


def sev(s):
    return [a for a, g in GOREV.items() if g[1] == s]


def satirlar(kol, kosu, adlar, kad, y, jeton, usd, yukseltme=0, ek=None):
    """toplu çağrının jetonu/USD'si görevlere eşit bölünür (shortcut: görev başı gerçek pay bilinmez); kayıt yalnız B'de"""
    sat = []
    for a in adlar:
        ok = bool(_guvenli(GOREV[a][3], y.get(a)))
        sat.append({"kol": kol, "kosu": kosu, "ad": a, "kademe": kad, "gecti": ok, "jeton": jeton / len(adlar),
                    "usd": usd / len(adlar), "yukseltme": yukseltme, **(ek or {})})
        if kol == "B":
            yonlendir.kaydet({**yonlendir.sec(GOREV[a][0]), **yonlendir.kurallar()["kademe"][kad], "kademe": kad,
                              **({"model": ek["model"]} if ek and ek.get("model") else {})}, "gecti" if ok else "kaldi",
                             {"giris": round(jeton / len(adlar))}, yukseltme,
                             {"ad": f"olcum-{a}", **({"yukseltme_sebep": "kota"} if ek and ek.get("kota") else {})})
    return sat


def sonnet(kol, kosu, adlar, kad, ham, yeniden, effort_kad=None, yukseltme=0):
    kd = {**yonlendir.kurallar()["kademe"][effort_kad or kad], "kademe": effort_kad or kad}
    y, jeton, usd = claude(toplu_istem(adlar, kosu), kd, ham, yeniden)
    return satirlar(kol, kosu, adlar, kad, y, jeton, usd, yukseltme)


def t0(kol, kosu):
    return [{"kol": kol, "kosu": kosu, "ad": a, "kademe": "T0", "gecti": bool(_guvenli(GOREV[a][3], GOREV[a][4]())), "jeton": 0,
             "usd": 0} for a in sev("T0")]


def kol_a(cikti, yeniden):
    """T1 ve T2 toplusu Sonnet high (T3 kademesinin bayrakları); T3 toplusu ortak"""
    return t0("A", 1) + sum((sonnet("A", 1, sev(k), k, cikti / f"A-1-{k}.json", yeniden, "T3") for k in ("T1", "T2")), [])


def kol_b(cikti, kosu, yeniden):
    sat = t0("B", kosu)
    ham = cikti / f"B-{kosu}-T1.json"
    if yeniden and ham.exists():
        r = json.loads(ham.read_text(encoding="utf-8"))
    else:
        r = yonlendir.t1(toplu_istem(sev("T1"), kosu), sor=_sor, haiku=_haiku)
        ham.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    u = r["usage"]
    sat += satirlar("B", kosu, sev("T1"), "T1", json_ilk(r["yanit"] or "") or {}, u["giris"] + u["cikis"], r["usd"],
                    ek={"model": r["model"], "kota": r["kota"], "sebep": ";".join(r["sebep"])})
    t2 = sev("T2") + [s["ad"] for s in sat if s["kademe"] == "T1" and not s["gecti"]]
    sat += sonnet("B", kosu, t2, "T2", cikti / f"B-{kosu}-T2.json", yeniden, yukseltme=0)
    kalan = [s["ad"] for s in sat if s["kademe"] == "T2" and not s["gecti"]]
    if kalan:  # tek yükseltme çağrısı (+1 → T3); tavan dolarsa görev kalır
        try:
            sat += sonnet("B", kosu, kalan, "T3", cikti / f"B-{kosu}-T3-yuk.json", yeniden, yukseltme=1)
        except RuntimeError:
            pass
    return sat


def sinif_dogruluk():
    """Yan ölçü: tür etiketi verilmeseydi sınıflayıcı (tek ücretsiz çağrı) doğru kademeyi bulur muydu? Jetonu B'ye eklenir."""
    dogru, jeton = 0, 0
    for a, (_, sev, istem, *_) in GOREV.items():
        r = yonlendir.sinifla(istem.split("\n")[0], sor=_sor, haiku=_haiku)
        dogru += r["kademe"] == sev
        jeton += sum((r.get("usage") or {}).get(k) or 0 for k in ("giris", "cikis"))
    return dogru, jeton


def main(cikti, yeniden=False):
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(cikti)
    cikti.mkdir(parents=True, exist_ok=True)
    ortak = sonnet("A", 1, sev("T3"), "T3", cikti / "AB-1-T3.json", yeniden)  # iki kolda birebir aynı çağrı
    a = kol_a(cikti, yeniden) + ortak
    sat = list(a)
    for kosu in (1, 2):
        sat += kol_b(cikti, kosu, yeniden) + [{**s, "kol": "B", "kosu": kosu, "ortak": 1} for s in ortak]
    sd, sj = (0, 0) if yeniden else sinif_dogruluk()
    alanlar = ["kol", "kosu", "ad", "kademe", "gecti", "jeton", "usd", "yukseltme", "model", "sebep", "ortak"]
    (cikti / "olcum.tsv").write_text("\n".join(["\t".join(alanlar)] + ["\t".join(str(s.get(k, "")) for k in alanlar) for s in sat]) + "\n",
                                     encoding="utf-8")
    oz = {"A_basari": sum(s["gecti"] for s in a), "A_jeton": round(sum(s["jeton"] for s in a)),
          "A_usd": round(sum(s["usd"] for s in a), 4), "kalan_A": [s["ad"] for s in a if not s["gecti"]]}
    for kosu in (1, 2):
        b = [s for s in sat if s["kol"] == "B" and s["kosu"] == kosu]
        son = {s["ad"]: s["gecti"] for s in b}  # yükseltme sonrası son durum (satır sırası)
        k = {"basari": sum(son.values()), "jeton": round(sum(s["jeton"] for s in b)), "usd": round(sum(s["usd"] for s in b), 4),
             "kalan": [x for x, v in son.items() if not v], "t1_model": next((s.get("model") for s in b if s["kademe"] == "T1"), None)}
        k["usd_azalma"] = round(1 - k["usd"] / oz["A_usd"], 3) if oz["A_usd"] else None
        k["jeton_azalma"] = round(1 - k["jeton"] / oz["A_jeton"], 3) if oz["A_jeton"] else None
        k["gecti"] = k["basari"] >= oz["A_basari"] and (k["usd_azalma"] or 0) >= 0.30
        oz[f"B{kosu}"] = k
    oz.update({"sinif_dogru": sd, "sinif_jeton": sj, "claude_p": Sayac.claude, "ucretsiz": Sayac.ucretsiz,
               "kart_karakter": len(KART), "KAPI": oz["B1"]["gecti"] and oz["B2"]["gecti"]})
    (cikti / "ozet.json").write_text(json.dumps(oz, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(oz, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], "--yeniden" in sys.argv)
