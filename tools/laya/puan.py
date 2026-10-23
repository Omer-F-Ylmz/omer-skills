"""Hakem yanıtından puan ayıklama (kurul.py 0-5, istem_dene.py 0-10). Yanıtın SON puanı geçerlidir; düşünme taslağı sayılmaz."""
import re

THINK = re.compile(r"<think(?:ing)?>.*?</think(?:ing)?>", re.S | re.I)
JSON_PUAN = re.compile(r'"score"\s*:\s*"?(\d+(?:\.\d+)?)"?')
SATIR_PUAN = re.compile(r"^\W*(?:score|puan)\W{0,3}(\d+(?:\.\d+)?)\W*$", re.I | re.M)


def ayikla(m, ust=5):
    """Son geçerli puan (float, 0..ust) ya da None. Kesik düşünme metni (JSON/tek satır puan yok) None döner."""
    m = THINK.sub("", m or "")
    bul = [x.group(1) for x in JSON_PUAN.finditer(m)] or [x.group(1) for x in SATIR_PUAN.finditer(m)]
    if not bul:
        return None
    p = float(bul[-1])
    return p if p <= ust and (ust == 10 or p == int(p)) else None
