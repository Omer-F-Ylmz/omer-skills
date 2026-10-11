"""KALİTE-3 Faz 2: skill klasörü → iyileştirilmiş kopya (orijinal dokunulmaz).

(a) gövde > 2k jeton ise çekirdek dışı ## bölümleri references/<slug>.md'ye TAŞINIR (silinmez);
    bilgi kontrol listesi (başlık · kural satırı · kod bloğu satırı) yeni yapıda aranır, eksik varsa kayıp döner.
(b) açıklamada tetik yoksa / kısaysa Messages Batch isteği (haiku yazar) JSONL'e eklenir; gönderim ayrı adım.
(c) kurulu olmayan mcp__<ad> eşleme tablosundaki kurulu karşılığa bağlanır; karşılık yoksa çekirdeğe not düşülür.
(d) çift birleştirme bu araçta yok: denetim TSV'sindeki cift>0 kayıtlar model adımında ele alınır.
python tools/skill_iyilestir.py <cikti_dizini> <skill_dizini>... [--istek istek.jsonl] [--esle esle.json]
"""
import argparse, json, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_filo_denetim import MCP, PD_SINIR, TETIK, ayir, jeton, mcp_adlari  # noqa: E402

YAZAR, DENETCI = "claude-haiku-5-5", "claude-sonnet-5-5"
# Çekirdekte kalır: tetik/ne zaman, iş akışı adımları, kurallar/yasaklar, çıktı biçimi, en fazla 1 kısa örnek.
CEKIRDEK = re.compile(r"when|use|usage|workflow|quick ?start|start|rule|step|stage|phase|overview|instruction|process|core|"
                      r"important|output|format|prohibit|never|must|don'?t|avoid|final|checklist|verif|"
                      r"kural|akış|adım|aşama|kullan|zaman|genel|önemli|talimat|çıktı|biçim|yasak", re.I)
# Taşınır (CEKIRDEK'i ezer): uzun örnekler, referans tabloları, API/parametre listeleri, şablonlar, ekler, SSS, geçmiş.
TASI = re.compile(r"example|örnek|reference|referans|table|tablo|\bapi\b|param|flag|option|seçenek|template|şablon|"
                  r"appendix|\bekler?\b|faq|\bsss\b|history|changelog|geçmiş|sürüm notu", re.I)
ORNEK = re.compile(r"example|örnek", re.I)
KURAL = re.compile(r"\b(MUST|NEVER|ALWAYS|DO NOT|ASLA|HER ZAMAN|YAPMA)\b")
DIZIN = re.compile(r"^#{3,4} +(.+?) *$|^ *[-*] +(?:`([^`\n]{2,40})`|\*\*([^*\n]{2,40})\*\*)", re.M)
KUCUK_BOLUM = 300
TR = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def bolumler(govde):
    """(giriş, [(başlık, metin)]); kod bloğu içindeki ## başlık sayılmaz."""
    parca, kod = [["", []]], False
    for satir in govde.splitlines(keepends=True):
        if satir.lstrip().startswith("```"):
            kod = not kod
        if not kod and satir.startswith("## "):
            parca.append([satir[3:].strip(), []])
        parca[-1][1].append(satir)
    return "".join(parca[0][1]), [(b, "".join(m)) for b, m in parca[1:]]


def kontrol(once, parcalar):
    """Eski gövdedeki başlık, kural ve kod satırlarından yeni parçalarda bulunmayanlar."""
    hepsi, eksik, kod = "\n".join(parcalar), [], False
    for satir in once.splitlines():
        s = satir.strip()
        if s.startswith("```"):
            kod = not kod
            continue
        if s and (kod or s.startswith("#") or KURAL.search(s)) and s not in hepsi:
            eksik.append(s)
    return eksik


def kurallar(icerik):
    """Kod bloğu dışındaki MUST/NEVER/ASLA... satırları."""
    kod, out = False, []
    for satir in icerik.splitlines():
        if satir.lstrip().startswith("```"):
            kod = not kod
        elif not kod and KURAL.search(satir):
            out.append(satir)
    return out


def _slug(baslik, kullanilan):
    s = re.sub(r"[^a-z0-9]+", "-", baslik.translate(TR).lower()).strip("-") or "bolum"
    aday, i = s, 2
    while aday in kullanilan:
        aday, i = f"{s}-{i}", i + 1
    kullanilan.add(aday)
    return aday


def iyilestir(kaynak, cikti, mcp, esle, istek=None, tavan=1024):
    kaynak, cikti = Path(kaynak), Path(cikti)
    shutil.copytree(kaynak, cikti, dirs_exist_ok=True)
    metin = (kaynak / "SKILL.md").read_text(encoding="utf-8")
    fm, govde = ayir(metin)
    ust = metin[: len(metin) - len(govde)]
    # (c) araç adları
    arac, notlar = [], []
    for ad in sorted(set(MCP.findall(govde))):
        if ad in mcp or ad.startswith("claude_ai_"):
            continue
        if esle.get(ad) in mcp:
            govde = govde.replace(f"mcp__{ad}__", f"mcp__{esle[ad]}__")
            arac.append(f"mcp__{ad}→mcp__{esle[ad]}")
        else:
            notlar.append(f"> Not (KALİTE-3): `mcp__{ad}` kurulu değil; bu adımlar o MCP kurulana dek çalışmaz.\n")
    once = jeton(govde)
    giris, bol = bolumler(govde)
    yeni, refler, kullanilan = [giris], [], {p.stem for p in (kaynak / "references").glob("*.md")}
    bolundu = once > PD_SINIR
    ornek_var = False
    for baslik, icerik in bol:
        kucuk = jeton(icerik) <= KUCUK_BOLUM
        if ORNEK.search(baslik):
            kal = kucuk and not ornek_var
            ornek_var |= kal
        else:
            kal = kucuk or (bool(CEKIRDEK.search(baslik)) and not TASI.search(baslik))
        if not bolundu or kal:
            yeni.append(icerik)
            continue
        ad = _slug(baslik, kullanilan)
        refler.append((ad, icerik))
        ilk = next((s.strip() for s in icerik.splitlines()[1:] if s.strip() and not s.lstrip().startswith(("#", "```"))), "")
        ozet = re.split(r"(?<=[.!?])\s", ilk)[0][:160]
        kural = "".join(f"{k}\n" for k in kurallar(icerik))  # taşınan bölümün kural satırları çekirdekte kalır
        # işaretçi dizin taşır: alt başlıklar + madde anahtarları; çıplak "Ayrıntı" kural adlarını gizliyordu (pilot ui-ux-pro-max)
        dizin = ", ".join(dict.fromkeys("".join(t) for t in DIZIN.findall(icerik)))[:400]
        icin = f" for: {dizin}" if dizin else ""
        yeni.append(f"## {baslik}\n\n{ozet}\n{kural}Read [references/{ad}.md](references/{ad}.md){icin}\n\n")
    if notlar:
        yeni.append("\n" + "".join(notlar))
    cekirdek = "".join(yeni)
    for ad, icerik in refler:
        (cikti / "references").mkdir(exist_ok=True)
        (cikti / "references" / f"{ad}.md").write_text(icerik, encoding="utf-8", newline="\n")
    (cikti / "SKILL.md").write_text(ust + cekirdek, encoding="utf-8", newline="\n")
    aciklama = fm.get("description", "")
    if istek and (len(aciklama) < 40 or not TETIK.search(aciklama)):
        istem = (f"Rewrite this Agent Skill description so Claude knows exactly when to trigger it. Keep every fact, "
                 f"add concrete trigger phrases ('Use when ...'), at most {tavan} characters, same language as the original. "
                 f"Reply with the description only.\n\nname: {fm.get('name', kaynak.name)}\ndescription: {aciklama}\n\n"
                 f"First 1500 characters of the body:\n{govde[:1500]}")
        with open(istek, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({"custom_id": f"aciklama-{kaynak.name}"[:64], "params": {
                "model": YAZAR, "max_tokens": 600, "messages": [{"role": "user", "content": istem}]}}, ensure_ascii=False) + "\n")
    return {"ad": fm.get("name", kaynak.name), "once": once, "sonra": jeton(cekirdek), "bolundu": bool(refler),
            "kayip": kontrol(govde, [cekirdek] + [i for _, i in refler]), "arac": arac, "not": len(notlar)}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cikti")
    ap.add_argument("skiller", nargs="+")
    ap.add_argument("--istek")
    ap.add_argument("--esle")
    a = ap.parse_args()
    esle = json.loads(Path(a.esle).read_text(encoding="utf-8")) if a.esle else {}
    mcp, hata = mcp_adlari(Path.home()), 0
    print("ad\tonce\tsonra\tbolundu\tkayip\tarac\tnot")
    for s in a.skiller:
        r = iyilestir(s, Path(a.cikti) / Path(s).name, mcp, esle, a.istek)
        hata += bool(r["kayip"])
        print(f"{r['ad']}\t{r['once']}\t{r['sonra']}\t{int(r['bolundu'])}\t{len(r['kayip'])}\t{';'.join(r['arac'])}\t{r['not']}")
    sys.exit(1 if hata else 0)


if __name__ == "__main__":
    main()
