"""ROUTER-1 (20 Eki) ölçüm kapısı: 12 görev (3 T0 · 3 kolay · 3 orta · 3 zor), (A) hepsi Sonnet high ↔ (B) tools/yonlendir.py.
A: tek toplu claude -p (12 görev). B: T0 betik · T1 ucuz_alt (ücretsiz) · T2 tek toplu (medium) · T3 tek toplu (high) ·
kalanlar için ≤1 yükseltme çağrısı (+1 kademe; T1 kalanı T2 topluna katılır). claude -p ≤4, ücretsiz ≤60.
Koşu 2 (kararlılık): B'nin T0+T1 kısmı + sınıflayıcı yok; Sonnet kısmının ikinci koşusu claude -p tavanına sığmaz.
Kabul her görevde yerel ve mekanik (test/şema/eşitlik) — denetçi modeli yok. Ham yanıtlar <çıktı>/ altında.
  python .kos/kopru/arka.py <günlük> .kos/kopru/olcum_sira.py tools/olcum/yonlendir_olc.py <çıktı_dizini> [--yeniden]"""
import json
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

CAGRI_TAVAN, USD_TAVAN, UCRETSIZ_TAVAN = 4, 0.6, 60
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
    "G02": ("bicim", "T0", "Ajan tanımlarının frontmatter'ından {dosya adı (uzantısız): model} JSON nesnesi çıkar.\n" + "\n".join(
        f"--- {p.name}\n" + "\n".join(p.read_text(encoding="utf-8").splitlines()[:6]) for p in sorted((KOK / ".claude/agents").glob("*.md"))),
        lambda y: y == AJAN, lambda: AJAN),
    "G03": ("birlestir", "T0", f"İki listenin birleşimi: tekil, Python sorted() sırasıyla JSON dizi.\nL1: {json.dumps(SKILL)}\n"
            f"L2: {json.dumps(sorted(AJAN))}", lambda y: y == BIRLESIM, lambda: BIRLESIM),
    "G04": ("lisans", "T1", "Bu lisans metninin SPDX kimliği nedir? Yanıt: SPDX dizgesi.\n" + oku(LIS["G04"], 1500),
            lambda y: bool(re.fullmatch(r"apache[- ]?(license[- ])?2\.0", str(y).strip().lower())), None),
    "G05": ("lisans", "T1", "Bu lisans metninin SPDX kimliği nedir? Yanıt: SPDX dizgesi.\n" + oku(LIS["G05"], 1500),
            lambda y: str(y).strip().lower() == "mit", None),
    "G06": ("etiket", "T1", f"Bu commit iletisinin iş türü hangisi? Seçenekler: {' | '.join(ETIKET)}. Yanıt: seçeneklerden biri.\n{COMMIT}",
            lambda y: str(y).strip() == "hata-duzelt", None),
    "G07": ("kod-oku", "T2", "Aşağıdaki modülde bayraklar('yargi', kademe=2) dönüşündeki --model ve --effort değerleri? "
            "Yanıt: {\"model\": ..., \"effort\": ...}\n" + oku("tools/model_sec.py"),
            lambda y: isinstance(y, dict) and (y.get("model"), y.get("effort")) == tuple(
                model_sec.bayraklar("yargi", kademe=2)[i] for i in (1, 3)), None),
    "G08": ("regex", "T2", "OmniRoute ücretsiz model kimliğini re.fullmatch ile tanıyan Python regex yaz: '/' ile ayrılmış en az iki boş "
            "olmayan parça (sağlayıcı/…/model), boşluk yok, kimlik ':free' ile biter ve ':free' yalnız sonda; combo adları "
            "(cc-ucuz-free gibi) eşleşmez. Örnek: openrouter/google/gemma-4-31b-it:free ✓, openrouter/x/y ✗. Yanıt: regex dizgesi.",
            lambda y: _regex_ok(y), None),
    "G09": ("alan-cikar", "T2", "Bu betik belgesindeki çıkış kodlarını {\"kod\": \"anlam\"} JSON nesnesi olarak çıkar.\n"
            + "\n".join(oku("tools/ucuz_alt.py").splitlines()[:9]), lambda y: isinstance(y, dict) and set(y) == {"0", "1", "3", "4"}, None),
    "G10": ("kod-yaz", "T3", "Yalnız stdlib ile `def json_al(y: str) -> dict | None` yaz: model yanıtındaki İLK GEÇERLİ JSON NESNESİNİ "
            "döndür; ```json çiti, önde/arkada düzyazı, dizgi içinde { } ve önce bozuk {…} parçası olabilir; dizi nesne sayılmaz; "
            "yoksa None. Yanıt: tam Python kodu (dizge).", lambda y: _kod_test(str(y), JSON_TEST), None),
    "G11": ("hata-duzelt", "T3", "Bu modülde bayraklar('yargi', kademe=2) IndexError veriyor. Kök nedeni bul; düzeltilmiş TAM modülü "
            "(import'lar dahil, __main__ bloğu olmadan) ver. Yanıt: Python kodu (dizge).\n" + BUGLI,
            lambda y: _kod_test(str(y), HATA_TEST), None),
    "G12": ("kod-yaz", "T3", "Yalnız stdlib ile `def sure_sn(s: str) -> float` yaz: '1:02:03'→3723, '02:03'→123, '1h2m3s'→3723, "
            "'45s'→45, '1.5m'→90, '2h'→7200, baş/son boşluk yok sayılır; geçersiz girdi ('', 'abc', '1:2:3:4', '5x') ValueError. "
            "Yanıt: tam Python kodu (dizge).", lambda y: _kod_test(str(y), SURE_TEST), None),
}


def _regex_ok(y):
    try:
        r = re.compile(str(y))
    except re.error:
        return False
    return all(r.fullmatch(s) for s in REGEX_POZ) and not any(r.fullmatch(s) for s in REGEX_NEG)


def toplu_istem(adlar, kart):
    g = "\n\n".join(f"## {a}\n{GOREV[a][2]}" for a in adlar)
    return ((KART + "\n\n") if kart else "") + (
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
                           input=istem, capture_output=True, text=True, encoding="utf-8", timeout=900, creationflags=0x08000000)
        ham.write_text(r.stdout, encoding="utf-8")
    try:
        d = json.JSONDecoder().raw_decode(ham.read_text(encoding="utf-8").lstrip())[0]
    except ValueError:  # boş/bozuk çıktı: görevler kalır, ham dosya incelemeye kalır
        return {}, 0, 0
    u = d.get("usage", {})
    jeton = sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
    return json_ilk(d.get("result", "")) or {}, jeton, d.get("total_cost_usd") or 0


def ucuz(ad, kosu, cikti):
    """T1: ucuz_alt.coz; istem başı koşu etiketi önbelleği deler (kararlılık koşusu gerçek çağrı olsun)."""
    tur, _, istem, *_ = GOREV[ad]
    secenek = ETIKET if tur == "etiket" else ()
    dosya = []
    if tur == "lisans":
        (f := cikti / f"{ad}-lisans.txt").write_text(oku(LIS[ad], 1500), encoding="utf-8")
        istem, dosya = "Bu lisans metninin SPDX kimliği nedir?", [str(f)]
    o, model, deneme, u, _ = ucuz_alt.coz(tur, f"[ROUTER-1 ölçüm koşu {kosu}] {istem}", dosya, secenek)
    Sayac.ucretsiz += deneme
    # shortcut: yalnız başarılı denemenin usage'ı sayılır (coz başarısızları döndürmez); çok denemede jeton eksik kalır
    return (o or {}).get("lisans" if tur == "lisans" else "etiket"), (u.get("prompt_tokens") or 0) + (u.get("completion_tokens") or 0), model


def kol_a(cikti, yeniden):
    adlar = list(GOREV)
    y, jeton, usd = claude(toplu_istem(adlar, False), yonlendir.sec("kod-yaz"), cikti / "A-1.json", yeniden)
    return [{"kol": "A", "kosu": 1, "ad": a, "kademe": "T3", "gecti": bool(_guvenli(GOREV[a][3], y.get(a))),
             "jeton": jeton / len(adlar), "usd": usd / len(adlar)} for a in adlar]


def _guvenli(f, y):
    try:
        return f(y)
    except Exception:
        return False


def kol_b(cikti, kosu, yeniden, sonnet=True):
    sat, bekle = [], {}
    for a, (tur, sev, _, kabul, betik) in GOREV.items():
        kd = yonlendir.sec(tur)
        assert kd["kademe"] == sev, (a, kd["kademe"])
        if sev == "T0":
            ok = _guvenli(kabul, betik())
            sat.append({"kol": "B", "kosu": kosu, "ad": a, "kademe": "T0", "gecti": ok, "jeton": 0, "usd": 0})
            yonlendir.kaydet(kd, "gecti" if ok else "kaldi", {}, 0, {"ad": f"olcum-{a}"})
        elif sev == "T1":
            y, jeton, model = ucuz(a, kosu, cikti)
            ok = _guvenli(kabul, y)
            sat.append({"kol": "B", "kosu": kosu, "ad": a, "kademe": "T1", "gecti": ok, "jeton": jeton, "usd": 0, "model": model})
            yonlendir.kaydet({**kd, "model": model or kd["model"]}, "gecti" if ok else "kaldi", {"giris": jeton}, 0, {"ad": f"olcum-{a}"})
            if not ok:
                bekle.setdefault("T2", []).append(a)
        else:
            bekle.setdefault(sev, []).append(a)
    if not sonnet:
        return sat
    kalan = {}
    for kad in ("T2", "T3"):
        if bekle.get(kad):
            sat += _toplu(bekle[kad], kad, cikti / f"B-{kosu}-{kad}.json", kosu, yeniden, kalan)
    if kalan:  # tek yükseltme çağrısı: en yüksek gereken kademede hepsi birlikte (shortcut: T2 kalanı T4'e çıkabilir)
        kad = max(kalan.values())
        sat += _toplu(list(kalan), kad, cikti / f"B-{kosu}-{kad}-yuk.json", kosu, yeniden, {}, yukseltme=1)
    return sat


def _toplu(adlar, kad, ham, kosu, yeniden, kalan, yukseltme=0):
    kd = {**yonlendir.kurallar()["kademe"][kad], "kademe": kad}
    y, jeton, usd = claude(toplu_istem(adlar, True), kd, ham, yeniden)
    sat = []
    for a in adlar:
        ok = bool(_guvenli(GOREV[a][3], y.get(a)))
        sat.append({"kol": "B", "kosu": kosu, "ad": a, "kademe": kad, "gecti": ok, "jeton": jeton / len(adlar), "usd": usd / len(adlar),
                    "yukseltme": yukseltme})
        # shortcut: toplu çağrının jetonu görevlere eşit bölünür; görev başı gerçek pay bilinmez
        yonlendir.kaydet({**yonlendir.sec(GOREV[a][0]), **kd}, "gecti" if ok else "kaldi",
                         {"giris": round(jeton / len(adlar))}, yukseltme, {"ad": f"olcum-{a}"})
        if not ok and kad != "T4":
            kalan[a] = yonlendir.SIRALI[yonlendir.SIRALI.index(kad) + 1]
    return sat


def sinif_dogruluk():
    """Yan ölçü: tür etiketi verilmeseydi sınıflayıcı (tek ücretsiz çağrı) doğru kademeyi bulur muydu? Jetonu B'ye eklenir."""
    dogru, jeton = 0, 0
    for a, (_, sev, istem, *_) in GOREV.items():
        r = yonlendir.sinifla(istem.split("\n")[0])
        Sayac.ucretsiz += 1
        dogru += r["kademe"] == sev
        jeton += sum((r.get("usage") or {}).get(k) or 0 for k in ("prompt_tokens", "completion_tokens"))
    return dogru, jeton


def main(cikti, yeniden=False):
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(cikti)
    cikti.mkdir(parents=True, exist_ok=True)
    sat = kol_a(cikti, yeniden) + kol_b(cikti, 1, yeniden) + kol_b(cikti, 2, yeniden, sonnet=False)
    sd, sj = (0, 0) if yeniden else sinif_dogruluk()
    alanlar = ["kol", "kosu", "ad", "kademe", "gecti", "jeton", "usd", "yukseltme", "model"]
    (cikti / "olcum.tsv").write_text("\n".join(["\t".join(alanlar)] + ["\t".join(str(s.get(k, "")) for k in alanlar) for s in sat]) + "\n",
                                     encoding="utf-8")
    a = [s for s in sat if s["kol"] == "A"]
    b = [s for s in sat if s["kol"] == "B" and s["kosu"] == 1]
    b_son = {s["ad"]: s["gecti"] for s in b}  # yükseltme sonrası son durum
    b1_ilk = {s["ad"]: s["gecti"] for s in b if s["kademe"] in ("T0", "T1")}  # kararlılık: ilk deneme ↔ koşu 2
    b2 = {s["ad"]: s["gecti"] for s in sat if s["kol"] == "B" and s["kosu"] == 2}
    oz = {"A_basari": sum(s["gecti"] for s in a), "B_basari": sum(b_son.values()),
          "A_jeton": round(sum(s["jeton"] for s in a)), "B_jeton": round(sum(s["jeton"] for s in b)) + sj,
          "A_usd": round(sum(s["usd"] for s in a), 4), "B_usd": round(sum(s["usd"] for s in b), 4),
          "B2_T0T1_ayni": b1_ilk == b2, "sinif_dogru": sd, "sinif_jeton": sj,
          "claude_p": Sayac.claude, "ucretsiz": Sayac.ucretsiz, "kalan_A": [s["ad"] for s in a if not s["gecti"]],
          "kalan_B": [k for k, v in b_son.items() if not v]}
    oz["jeton_azalma"] = round(1 - oz["B_jeton"] / oz["A_jeton"], 3) if oz["A_jeton"] else None
    oz["KAPI"] = oz["B_basari"] >= oz["A_basari"] and (oz["jeton_azalma"] or 0) >= 0.30 and oz["B2_T0T1_ayni"]
    (cikti / "ozet.json").write_text(json.dumps(oz, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(oz, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], "--yeniden" in sys.argv)
