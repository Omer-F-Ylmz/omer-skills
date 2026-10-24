"""claude-code-mods açılış yaması (BASLANGIC-HIZ-2 P3/P4).

Her hook modülü `session.start` içinde `$.command.register` çağırır; host her çağrıda eklenti taramasını
yeniden yapar (27 çağrı → 28 geçiş). Bu betik çağrıyı ilk `ui.render` (AbovePrompt) içine bayraklı tek
seferlik `void` çağrı olarak taşır. Kalıp tutmayan mod ATLANIR (Pane-only render, erken return, vb.).

  python tools/mod_yama.py --uygula | --geri | --durum

Kayıt: .kos/kopru/mod-yama.json (mod → SHA-256'lar); yedek: .kos/kopru/yedek/mod-yama/<mod>/.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
MODS = Path.home() / ".claude/plugins/marketplaces/claude-code-mods/mods"
KAYIT = KOK / ".kos/kopru/mod-yama.json"
YEDEK = KOK / ".kos/kopru/yedek/mod-yama"

REG = re.compile(r"^(?P<ind>[ \t]*)await (?P<call>\$\.command\.register\(.*\)\.catch\(\(\) => \{\}\))(?P<yor>[ \t]*//.*)?\n", re.M)
RENDER = re.compile(
    r"on\('ui\.render', \{ component: 'AbovePrompt' \}, async \(\$, e, next\) => \{\n(?P<ind>[ \t]*)const rest = await next\(e\)[^\n]*\n"
)
EXPORT = re.compile(r"^export const register: Register", re.M)


def yamala(text):
    """LF'li metin → (yamalı metin, None) ya da (None, atlama nedeni)."""
    if "cmdRegistered" in text:
        return None, "zaten yamalı"
    kayitlar = list(REG.finditer(text))
    if len(kayitlar) != 1:
        return None, f"register satırı {len(kayitlar)} (1 beklenir)"
    r = kayitlar[0]
    basla = text.rfind("on('session.start'", 0, r.start())
    if basla < 0:
        return None, "register session.start içinde değil"
    if re.search(r"\breturn\b", text[basla:r.start()]):
        return None, "register'dan önce erken return (koşullu kayıt)"
    m = RENDER.search(text)
    if not m or not EXPORT.search(text):
        return None, "AbovePrompt ui.render yok (Pane-only: komut açılmadan render olmaz)"
    ind = m.group("ind")
    ekle = (f"{ind}if (!cmdRegistered) {{\n{ind}  cmdRegistered = true\n"
            f"{ind}  void {r.group('call')}{r.group('yor') or ''}\n{ind}}}\n")
    # sonraki konumdan önce işle ki öncekinin ofseti bozulmasın
    if r.start() < m.end():
        t = text[:m.end()] + ekle + text[m.end():]
        t = t[:r.start()] + t[r.end():]
    else:
        t = text[:r.start()] + text[r.end():]
        t = t[:m.end()] + ekle + t[m.end():]
    return EXPORT.sub("let cmdRegistered = false\n\nexport const register: Register", t, count=1), None


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dosya(mods, mod):
    adaylar = sorted((mods / mod / "hooks").glob("register.ts*"))
    return adaylar[0] if adaylar else None


def modlar(mods):
    return sorted(p.name for p in mods.iterdir() if p.is_dir() and dosya(mods, p.name))


def yukle(kayit):
    return json.loads(kayit.read_text(encoding="utf8")) if kayit.exists() else {}


def kaydet(kayit, durum):
    kayit.parent.mkdir(parents=True, exist_ok=True)
    kayit.write_text(json.dumps(durum, indent=2, ensure_ascii=False), encoding="utf8")


def uygula(mods, kayit, yedek):
    durum, ok = yukle(kayit), 0
    for mod in modlar(mods):
        p = dosya(mods, mod)
        ham = p.read_bytes()
        e = durum.get(mod)
        if e and sha(ham) == e["yamali"]:
            print(f"{mod}: yamalı (değişmedi)")
            ok += 1
            continue
        yeni, neden = yamala(ham.decode("utf8").replace("\r\n", "\n"))
        if yeni is None:
            print(f"{mod}: ATLANDI — {neden}")
            continue
        nl = "\r\n" if b"\r\n" in ham else "\n"
        yamali = yeni.replace("\n", nl).encode("utf8")
        y = yedek / mod / p.name
        y.parent.mkdir(parents=True, exist_ok=True)
        y.write_bytes(ham)
        p.write_bytes(yamali)
        durum[mod] = {"dosya": p.name, "orijinal": sha(ham), "yamali": sha(yamali), "yedek": str(y)}
        print(f"{mod}: yamalandı")
        ok += 1
    kaydet(kayit, durum)
    print(f"{ok} mod yamalı")
    return 0


def geri(mods, kayit, yedek):
    durum = yukle(kayit)
    for mod, e in list(durum.items()):
        p = mods / mod / "hooks" / e["dosya"]
        cur = sha(p.read_bytes()) if p.exists() else None
        if cur == e["yamali"]:
            y = Path(e["yedek"])
            if not y.exists() or sha(y.read_bytes()) != e["orijinal"]:
                print(f"{mod}: HATA — yedek yok/bozuk, dokunulmadı")
                continue
            shutil.copyfile(y, p)
            del durum[mod]
            print(f"{mod}: geri alındı")
        elif cur == e["orijinal"]:
            del durum[mod]
            print(f"{mod}: zaten orijinal")
        else:
            print(f"{mod}: UYARI — güncellenmiş, dokunulmadı")
    kaydet(kayit, durum)
    return 0


def durum_yaz(mods, kayit):
    durum = yukle(kayit)
    for mod in modlar(mods):
        p = dosya(mods, mod)
        cur, e = sha(p.read_bytes()), durum.get(mod)
        if e and cur == e["yamali"]:
            s = "yamalı"
        elif e and cur != e["orijinal"]:
            s = "güncellenmiş"
        else:
            neden = yamala(p.read_bytes().decode("utf8").replace("\r\n", "\n"))[1]
            s = "temiz (yamalanabilir)" if neden is None else f"temiz (atlanır: {neden})"
        print(f"{mod}: {s}")
    return 0


def main(argv=None):
    a = argparse.ArgumentParser()
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--uygula", action="store_true")
    g.add_argument("--geri", action="store_true")
    g.add_argument("--durum", action="store_true")
    a.add_argument("--mods-dir", type=Path, default=MODS)
    a.add_argument("--kayit", type=Path, default=KAYIT)
    a.add_argument("--yedek", type=Path, default=YEDEK)
    n = a.parse_args(argv)
    if n.uygula:
        return uygula(n.mods_dir, n.kayit, n.yedek)
    if n.geri:
        return geri(n.mods_dir, n.kayit, n.yedek)
    return durum_yaz(n.mods_dir, n.kayit)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
