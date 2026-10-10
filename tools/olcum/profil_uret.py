"""KÜTÜPHANE-4: name-only profil üretici. Bir ölçüm koşusunun init ad listesinden (docs/kutuphane/olcum/<tarih>-<profil>-init.json)
henüz skillOverrides'ta olmayan her skill'i "name-only" yapan TAM skillOverrides bloğunu yazar (mevcut kullanıcı kararları korunur).
Yönlendirici (departman-*) ve Ömer'in çekirdek skill'leri açıklamalı kalır (KORU). settings.json'a dokunmaz; yalnız okur.
  python tools/olcum/profil_uret.py --init docs/kutuphane/olcum/2026-10-10-tam-init.json [--cikti tools/olcum/profil-nameonly.json]"""
import argparse
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KORU = [r"(^|:)departman-", r"(^|:)frontend-craft$", r"(^|:)impeccable$", r"(^|:)frontend-design$", r"(^|:)ui-ux-pro-max$",
        r"(^|:)graphify", r"blender", r"(^|:)using-superpowers$", r"(^|:)(pdf|docx|pptx|xlsx)$",
        r"(^|:)(omer-kutuphaneler|web-sahne-desenleri|sdp|surec|gorsel-uret|mod-atolyesi|prd-yaz|teklif-kutusu|fatura-kutusu|headroom-compress|jev)$",
        r"(^|:)video-(izle|uygula|tarama)$", r"-desktop$"]


def koru(ad):
    return any(re.search(k, ad) for k in KORU)


def uret(skills, mevcut):
    yeni = {ad: "name-only" for ad in skills if ad not in mevcut and not koru(ad)}
    return {**mevcut, **yeni}, len(yeni), sorted(ad for ad in skills if ad not in mevcut and koru(ad))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--init", required=True)
    p.add_argument("--cikti", default=str(KOK / "tools" / "olcum" / "profil-nameonly.json"))
    p.add_argument("--ayar", default=str(Path.home() / ".claude" / "settings.json"))
    ns = p.parse_args(argv)
    skills = json.loads((KOK / ns.init).read_text(encoding="utf-8")).get("skills") or []
    mevcut = json.loads(Path(ns.ayar).read_text(encoding="utf-8")).get("skillOverrides") or {}
    blok, n, korunan = uret(skills, mevcut)
    Path(ns.cikti).write_text(json.dumps({"skillOverrides": blok}, ensure_ascii=False, indent=1), encoding="utf-8")
    deg = {}
    for v in mevcut.values():
        deg[v] = deg.get(v, 0) + 1
    print(f"init skill {len(skills)} · mevcut override {len(mevcut)} {deg} · yeni name-only {n} · korunan {len(korunan)}")
    print("korunan:", ", ".join(korunan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
