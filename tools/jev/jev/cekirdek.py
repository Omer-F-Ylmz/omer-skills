"""Jev çekirdeği: arka uç seçimi, tek boğaz noktası (tavan → redaksiyon → bölme → parça → tekrar), bantlar, tablo.

Anahtar yalnız istek başlığına girer; gövde ve anahtar hiçbir çıktıya, hata metnine ya da dosyaya yazılmaz.
"""
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

MODELLER = ("jev-1.13", "jev-latest")
PARCA = 200
STATE_TOKEN = 32_000
TEKRAR = 2
VARSAYILAN_BANT = {"act": 0.85, "flag": 0.60}
BANT_YOLU = Path.home() / ".config" / "jev" / "bantlar.json"
MCP_URL = "https://jev-mcp-lemon.vercel.app/mcp"
ANAHTAR_ADLARI = ("TYPESAFE_API_KEY", "OPENROUTER_API_KEY", "JEV_MCP_TOKEN")


class JevHata(Exception):
    pass


class TavanHata(JevHata):
    pass


class AnahtarYok(JevHata):
    pass


def backend(env):
    if env.get("TYPESAFE_API_KEY"):
        return {"ad": "TYPESAFE", "url": "https://api.typesafe.ai/v1/systemone", "anahtar": env["TYPESAFE_API_KEY"]}
    if env.get("OPENROUTER_API_KEY"):
        return {"ad": "OPENROUTER", "url": "https://openrouter.ai/api/v1/systemone", "anahtar": env["OPENROUTER_API_KEY"]}
    if env.get("JEV_MCP_TOKEN"):
        return {"ad": "MCP", "url": MCP_URL, "anahtar": env["JEV_MCP_TOKEN"]}
    return None


def _luhn(rakam):
    t = 0
    for i, d in enumerate(map(int, reversed(rakam))):
        t += d if i % 2 == 0 else (d * 2 - 9 if d > 4 else d * 2)
    return t % 10 == 0


# Sıra önemli: anahtarlar ve IBAN, içlerindeki rakamları kart/TCKN desenleri yemeden önce.
REDAKSIYON = [
    ("anahtar", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}|\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_\w{40,}"
                           r"|\bAKIA[0-9A-Z]{16}\b|\bxox[bpas]-[A-Za-z0-9-]{10,}|\bAIza[0-9A-Za-z_-]{35}|(?i:bearer)\s+\S{16,}")),
    ("iban", re.compile(r"\bTR\d{2}(?:\s?\d{4}){5}\s?\d{2}\b", re.I)),
    ("kart", re.compile(r"\b\d(?:[ -]?\d){12,18}\b")),
    ("tckn", re.compile(r"\b[1-9]\d{10}\b")),
    ("telefon", re.compile(r"(?:\+90|\b0)[\s-]?\(?[2-5]\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}\b")),
    ("e-posta", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
]


def redakte(metin):
    for tur, desen in REDAKSIYON:
        if tur == "kart":
            metin = desen.sub(lambda m: "[REDAKTE:kart]" if _luhn(re.sub(r"\D", "", m[0])) else m[0], metin)
        else:
            metin = desen.sub(f"[REDAKTE:{tur}]", metin)
    return metin


# ponytail: tokenizer yok, 13a ile aynı UTF-8 bayt/4 kaba tahmin; kesin sınır sunucunun 422'si.
def token(s):
    return math.ceil(len(s.encode()) / 4)


def bol_state(s, ust=STATE_TOKEN - 2_000):
    """Soruya pay bırakarak ≤ust token parçalara satır sınırından böler; tek satır taşarsa karakterle keser."""
    if token(s) <= ust:
        return [s]
    sinir, parcalar, cur, n = ust * 4, [], [], 0
    for satir in s.splitlines(keepends=True):
        for i in range(0, len(satir), ust):  # ≤4 bayt/karakter → ≤ust*4 bayt
            p = satir[i:i + ust]
            b = len(p.encode())
            if cur and n + b > sinir:
                parcalar.append("".join(cur))
                cur, n = [], 0
            cur.append(p)
            n += b
    if cur:
        parcalar.append("".join(cur))
    return parcalar


def parcala(xs, n=PARCA):
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def kesinlik(cevap):
    if cevap["type"] == "noul":
        return max(cevap["noul"], 1 - cevap["noul"])
    return cevap.get("confidence", 0.0)


def bant(k, b):
    return "Act" if k >= b["act"] else "Flag" if k >= b["flag"] else "Escalate"


def bantlar_oku(yol=None):
    yol = Path(yol or BANT_YOLU)
    try:
        v = json.loads(yol.read_text(encoding="utf-8"))
        return {"act": float(v["act"]), "flag": float(v["flag"])}
    except FileNotFoundError:
        print(f"uyarı: {yol} yok, varsayılan bantlar 0.85/0.60 (ölçmek için: jev kalibre)", file=sys.stderr)
        return dict(VARSAYILAN_BANT)


def tablo(basliklar, satirlar, ust=25):
    hucre = lambda x: str(x).replace("|", "/").replace("\n", " ")[:80]
    govde = ["| " + " | ".join(map(hucre, r)) + " |" for r in satirlar]
    if len(govde) > ust - 2:
        govde = govde[:ust - 3] + [f"… +{len(satirlar) - (ust - 3)} satır; tamamı için --json"]
    return "\n".join(["| " + " | ".join(basliklar) + " |", "|" + "---|" * len(basliklar)] + govde)


def http_gonder(url, basliklar, govde, timeout=60):
    istek = urllib.request.Request(url, data=govde, headers=basliklar, method="POST")
    try:
        with urllib.request.urlopen(istek, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read()


def _bekle(basliklar, deneme):
    ra = {k.lower(): v for k, v in basliklar.items()}.get("retry-after")
    try:
        return min(float(ra), 30.0)
    except (TypeError, ValueError):
        return 2 ** deneme


def _tur(yanit):
    """Hata gövdesinden yalnız tür adı; mesaj (girdi yankısı, anahtar) asla."""
    try:
        j = json.loads(yanit)
        e = j.get("error")
        t = j.get("error_type") or (e.get("type") or e.get("code") if isinstance(e, dict) else None)
        return t if isinstance(t, str) and re.fullmatch(r"[\w.-]{1,40}", t) else "?"
    except (ValueError, AttributeError):
        return "?"


def _json(yanit):
    metin = yanit.decode("utf-8", "replace")
    if metin.lstrip().startswith(("event:", "data:")):  # SSE: son data satırı
        metin = [s[5:] for s in metin.splitlines() if s.startswith("data:")][-1]
    return json.loads(metin)


def _en_belirsiz(a, b):
    if a is None or b is None:
        return None
    return {ad: min(a[ad], b[ad], key=kesinlik) for ad in a}


_YOK = object()


class Tasiyici:
    def __init__(self, env=None, en_fazla=5, model="jev-1.13", gonder=None, uyu=time.sleep, istek_tavan=250, tekrar=TEKRAR):
        if model not in MODELLER:
            raise JevHata(f"model yalnız {' | '.join(MODELLER)}")
        self.b = backend(os.environ if env is None else env)
        if self.b is None:
            raise AnahtarYok("anahtar yok; ortamda şunlardan biri gerekli: " + " / ".join(ANAHTAR_ADLARI))
        self.en_fazla, self.model, self.gonder, self.uyu, self.cagri = en_fazla, model, gonder or http_gonder, uyu, 0
        self.istek_tavan, self.istek, self.tekrar, self.kullanim = istek_tavan, 0, tekrar, []

    def yargila(self, states, questions):
        """Tek boğaz noktası. İki tavan: batch (≤200 state) ve HTTP isteği (tekrarlar dahil); ikisi de ağa çıkmadan kontrol edilir."""
        duz, kaynak = [], []
        for i, s in enumerate(states):
            for p in bol_state(redakte(s)):
                duz.append(p)
                kaynak.append(i)
        parcalar = parcala(duz)
        if self.cagri + len(parcalar) > self.en_fazla:
            raise TavanHata(f"tavan: {len(parcalar)} çağrı gerekiyor, kalan {self.en_fazla - self.cagri} (--en-fazla)")
        gerekli = len(parcalar) if self.b["ad"] == "MCP" else len(duz)
        if self.istek + gerekli > self.istek_tavan:
            raise TavanHata(f"istek tavanı: en az {gerekli} HTTP isteği gerekiyor, kalan {self.istek_tavan - self.istek} (--istek-tavan)")
        cevaplar = []
        for p in parcalar:
            self.cagri += 1
            cevaplar += self._mcp(p, questions) if self.b["ad"] == "MCP" else [self._api(s, questions) for s in p]
        sonuc = [_YOK] * len(states)
        for i, cv in zip(kaynak, cevaplar):
            sonuc[i] = cv if sonuc[i] is _YOK else _en_belirsiz(sonuc[i], cv)  # bölünen state: parçaların en belirsizi
        return sonuc

    def _istek(self, govde, basliklar):
        veri = json.dumps(govde, ensure_ascii=False).encode()
        for deneme in range(self.tekrar + 1):
            if self.istek >= self.istek_tavan:
                raise TavanHata(f"istek tavanı: {self.istek_tavan} HTTP isteği doldu (tekrarlar dahil, --istek-tavan)")
            self.istek += 1
            try:
                status, hdr, yanit = self.gonder(self.b["url"], basliklar, veri)
            except OSError:
                raise JevHata(f"{self.b['ad']}: bağlanılamadı") from None
            if status < 400:
                return _json(yanit)
            if deneme < self.tekrar and (status in (408, 429) or status >= 500):
                self.uyu(_bekle(hdr, deneme))
                continue
            raise JevHata(f"sağlayıcı {status} ({_tur(yanit)})")

    def _api(self, state, questions):
        basliklar = {"Authorization": f"Bearer {self.b['anahtar']}", "Content-Type": "application/json"}
        j = self._istek({"model": self.model, "state": state, "questions": questions}, basliklar)
        self.kullanim.append(j.get("usage") or {})
        return j["answers"]

    def _mcp(self, states, questions):
        basliklar = {"x-api-key": self.b["anahtar"], "Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        govde = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                 "params": {"name": "jev_batch", "arguments": {"states": states, "questions": questions, "model": self.model}}}
        r = self._istek(govde, basliklar)
        if "error" in r or r.get("result", {}).get("isError"):
            raise JevHata("MCP jev_batch hata döndü")
        liste = sorted(json.loads(r["result"]["content"][0]["text"]), key=lambda x: x["index"])
        return [x["answers"] if x.get("ok") else None for x in liste]
