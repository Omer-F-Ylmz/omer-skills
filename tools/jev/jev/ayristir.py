"""Kodla ayrıştırma: Jev'e gitmeden önce hatalar, parçalar, iddialar ve bulgular burada çıkarılır."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from .cekirdek import redakte

# --- log ---
TEST = re.compile(r"^\s*(?:Failed (\S+) \[|failed (\S+) \()")  # VSTest · MTP
TEST_SON = re.compile(r"^\s*(?:Passed|Skipped|passed|skipped) ")
DERLEME = re.compile(r"^\s*(.*?)\((\d+),\d+\): error ([A-Z]+\d+): (.*?)(?: \[[^\]]*\])?$")
DERLEME_YALIN = re.compile(r"\berror ([A-Z]{2,}\d{3,}): (.*?)(?: \[[^\]]*\])?$")
PYTEST = re.compile(r"^(FAILED|ERROR) (\S+)(?: - (.*))?$")


def log_hatalari(metin):
    if "<TestRun" in metin[:1000]:
        return _trx(metin)
    if "short test summary info" in metin:
        return _pytest(metin)
    return _dotnet(metin)


def _trx(metin):
    if "<!DOCTYPE" in metin or "<!ENTITY" in metin:  # trx'te DTD olmaz; entity genişletme yolunu kapat
        raise ValueError("trx DTD/ENTITY içeriyor, okunmadı")
    out = []
    for e in ET.fromstring(metin.encode()).iter():
        if e.tag.endswith("UnitTestResult") and e.get("outcome") == "Failed":
            ayrinti = "\n".join((x.text or "").strip() for x in e.iter() if x.tag.endswith(("Message", "StackTrace")))
            out.append({"ad": e.get("testName"), "metin": ayrinti})
    return out


def _pytest(metin):
    bolum = metin.split("short test summary info", 1)[1]
    bloklar = dict(re.findall(r"^_{3,} (.+?) _{3,}\n(.*?)(?=^_{3,} |^={3,})", metin, re.M | re.S))
    out = []
    for s in bolum.splitlines():
        m = PYTEST.match(s)
        if m:
            kisa = m[2].split("::")[-1]
            detay = next((v for k, v in bloklar.items() if k.endswith(kisa)), "")
            out.append({"ad": m[2], "metin": f"{m[1]} {m[3] or ''}\n{detay[-1500:]}".strip()})
    return out


def _dotnet(metin):
    satirlar, out, gorulen = metin.splitlines(), [], set()
    for i, s in enumerate(satirlar):
        m = TEST.match(s)
        if m:
            blok = []
            for t in satirlar[i + 1:i + 40]:
                if TEST.match(t) or TEST_SON.match(t) or not t.strip():
                    break
                blok.append(t.strip())
            out.append({"ad": m[1] or m[2], "metin": "\n".join(blok)})
            continue
        m = DERLEME.match(s)
        anahtar = (m[1], m[2], m[3]) if m else None
        if not m and (y := DERLEME_YALIN.search(s)):
            anahtar = ("", y[1], y[2])
        if anahtar and anahtar not in gorulen:  # MSBuild hataları özette tekrarlar
            gorulen.add(anahtar)
            ad = f"{re.split(r'[\\/]', m[1])[-1]}:{m[2]} {m[3]}" if m else y[1]
            out.append({"ad": ad, "metin": m[4] if m else y[2]})
    return out


# --- ilgili ---
SINIR = {
    ".py": r"^\s*(?:async\s+def|def|class)\s",
    ".cs": r"^\s*(?:\[.*\]\s*)?(?:(?:public|private|protected|internal|static|async|override|virtual|sealed|abstract|partial|readonly)\s+)+\S"
           r"|^\s*(?:namespace|class|interface|struct|enum|record)\s",
}
SINIR_TS = r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function|class|interface|type|enum)\b|^\s*(?:export\s+)?const\s+\w+\s*=\s*(?:async\s*)?(?:\(|function)"
for _uz in (".ts", ".tsx", ".js", ".mjs", ".jsx"):
    SINIR[_uz] = SINIR_TS


def parcala_dosya(yol, metin, ust=80):
    """≤ust satırlık (bas, son) aralıkları; mümkünse son tip/fonksiyon sınırından önce keser."""
    satirlar = metin.splitlines()
    desen = SINIR.get(Path(yol).suffix.lower())
    sinirlar = {i + 1 for i, s in enumerate(satirlar) if desen and re.match(desen, s)}
    out, bas, n = [], 1, len(satirlar)
    while bas <= n:
        son = min(bas + ust - 1, n)
        if son < n and (aday := [b for b in sinirlar if bas < b <= son + 1]):
            son = max(aday) - 1
        out.append((bas, son))
        bas = son + 1
    return out


# --- kanit ---
def iddialar(metin):
    out, kod = [], False
    for n, s in enumerate(metin.splitlines(), 1):
        t = s.strip()
        if t.startswith("```"):
            kod = not kod
            continue
        if kod or not t or t.startswith(("#", "|")):
            continue
        t = re.sub(r"^(?:[-*+>]|\d+[.)])\s+", "", t)
        if t:
            out.append((n, t))
    return out


# --- triage ---
GITLEAKS_GIZLI = ("Secret", "Match", "Line")


def _kayit(kural, dosya, satir, **baglam):
    state = redakte(json.dumps({"kural": kural, "dosya": dosya, "satir": satir, **baglam}, ensure_ascii=False, default=str))
    return {"kural": str(kural), "dosya": str(dosya), "satir": satir, "state": state}


def bulgular(veri):
    """semgrep · gitleaks · SARIF · SkillSpector · axe JSON → [{kural, dosya, satir, state}]. Gizli değerler state'e girmez."""
    if isinstance(veri, list) and veri and isinstance(veri[0], dict) and "RuleID" in veri[0]:  # gitleaks
        out = []
        for b in veri:
            temiz = {k: v for k, v in b.items() if k not in GITLEAKS_GIZLI}
            out.append(_kayit(temiz.pop("RuleID"), temiz.pop("File", ""), temiz.pop("StartLine", None), **temiz))
        return out
    if isinstance(veri, list):  # axe sonuç listesi (genişlik başına)
        return [b for x in veri for b in bulgular(x)]
    if "results" in veri:  # semgrep; extra.lines / metavars eşleşen değeri taşır, alınmaz
        return [_kayit(r["check_id"], r["path"], r["start"]["line"], mesaj=r["extra"].get("message"), onem=r["extra"].get("severity"))
                for r in veri["results"]]
    if "runs" in veri:  # SARIF
        out = []
        for run in veri["runs"]:
            for r in run.get("results", []):
                loc = (r.get("locations") or [{}])[0].get("physicalLocation", {})
                out.append(_kayit(r.get("ruleId"), loc.get("artifactLocation", {}).get("uri", ""), loc.get("region", {}).get("startLine"),
                                  mesaj=r.get("message", {}).get("text"), seviye=r.get("level")))
        return out
    if "violations" in veri:  # axe
        return [_kayit(v["id"], veri.get("url", ""), None, etki=v.get("impact"), yardim=v.get("help"), dugum=len(v.get("nodes", [])))
                for v in veri["violations"]]
    if "findings" in veri:  # SkillSpector (şema varsayımı: rule_id/file/line/severity/message)
        return [_kayit(f.get("rule_id") or f.get("rule") or f.get("id"), f.get("file") or f.get("path", ""), f.get("line"),
                       seviye=f.get("severity"), mesaj=f.get("message") or f.get("description") or f.get("title"))
                for f in veri["findings"]]
    raise ValueError("tanınmayan bulgu biçimi (semgrep · gitleaks · SARIF · SkillSpector · axe JSON)")
