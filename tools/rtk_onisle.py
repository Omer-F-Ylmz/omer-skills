"""PreToolUse(Bash|PowerShell) ön-işleyici (TOKEN-7a 2b): rtk hook claude'un
yeniden yazmadığı aileleri `rtk <komut>` biçimine çevirir. rtk zaten yazıyorsa
sessiz kalır (iki kanca aynı girdiye updatedInput vermesin). Bilinmeyen ya da
çözülemeyen girdi özgün bayt kalır: çıktı yok, çıkış 0.
Kanca: ~/.claude/hooks/rtk-onisle.py bu modülün main()'ini çağırır."""
import json
import re
import subprocess
import sys

# Her iki kabukta güvenli aileler; Bash'e ek olarak grep/ls/wc (içerik dökenler yok).
ORTAK = [
    (re.compile(r"git(?=\s|$)"), "rtk git"),
    (re.compile(r"dotnet(?=\s|$)"), "rtk dotnet"),
    (re.compile(r"npm(?:\.cmd)?(?=\s|$)"), "rtk npm"),
    (re.compile(r"(?:python3?\s+-m\s+)?pytest(?=\s|$)"), "rtk pytest"),
    (re.compile(r"node(?=\s+--test(?:\s|$))"), "rtk node"),
]
BASH_EK = [(re.compile(r"(grep|ls|wc)(?=\s|$)"), r"rtk \1")]

# Üst düzey ayraçlar: &&, ||, ;, |. Pipe sonrası parça tüketicidir (head, Select-Object): dokunulmaz.
AYRAC = re.compile(r"&&|\|\||;|\|")


def parcala(komut):
    """Tırnak dışı ayraçlarda böl; [(parça, ayraç)]. Kapanmamış tırnak → None."""
    out, bas, tirnak, i = [], 0, None, 0
    while i < len(komut):
        c = komut[i]
        if tirnak:
            if c == tirnak:
                tirnak = None
        elif c in "'\"":
            tirnak = c
        elif c == "`" or komut.startswith("$(", i):
            return None  # alt kabuk / PS kaçışı: çözülemez, dokunma
        else:
            m = AYRAC.match(komut, i)
            if m:
                out.append((komut[bas:i], m.group()))
                i = bas = m.end()
                continue
        i += 1
    if tirnak:
        return None
    out.append((komut[bas:], ""))
    return out


def yeniden_yaz(komut, arac):
    parcalar = parcala(komut)
    if not parcalar:
        return None
    kurallar = ORTAK + (BASH_EK if arac == "Bash" else [])
    sonuc, onceki, degisti = [], "", False
    for parca, ayrac in parcalar:
        govde = parca.lstrip()
        bosluk = parca[: len(parca) - len(govde)]
        if onceki != "|" and not govde.startswith("rtk "):
            for desen, hedef in kurallar:
                m = desen.match(govde)
                if m:
                    govde = m.expand(hedef) + govde[m.end():]
                    degisti = True
                    break
        sonuc.append(bosluk + govde + ayrac)
        onceki = ayrac
    return "".join(sonuc) if degisti else None


def rtk_yaziyor(ham):
    try:
        r = subprocess.run(["rtk", "hook", "claude"], input=ham, capture_output=True,
                           text=True, encoding="utf-8", timeout=10)
        return bool(r.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        return False


# TOKEN-REA rtk2: süzgeçli tek komut rtk2'ye yazılır (rtk2.tur); tırnak/ayraç/yönlendirme olan komuta dokunmaz.
def rtk2_yaz(komut):
    if AYRAC.search(komut) or any(c in komut for c in "\"'`$<>"):
        return None
    import importlib.util, os
    yol = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".kos", "kopru", "token-rea", "rtk2.py")
    if not os.path.exists(yol):
        return None
    ozel = importlib.util.spec_from_file_location("rtk2", yol)
    m = importlib.util.module_from_spec(ozel)
    ozel.loader.exec_module(m)
    argv = komut.split()
    return f"python -I -S {yol} {komut.strip()}" if argv and m.tur(argv) in ("ls", "diff", "durum") else None


def main(stdin=sys.stdin, stdout=sys.stdout, rtk_kontrol=rtk_yaziyor):
    ham = stdin.read().lstrip("﻿")
    try:
        veri = json.loads(ham)
        arac = veri["tool_name"]
        komut = veri["tool_input"]["command"]
    except (ValueError, KeyError, TypeError):
        return 0
    if arac not in ("Bash", "PowerShell") or not isinstance(komut, str) or not komut.strip():
        return 0
    r2 = rtk2_yaz(komut) if arac == "Bash" else None  # TOKEN-REA rtk2
    yeni = r2 or yeniden_yaz(komut, arac)
    if yeni is None or (r2 is None and rtk_kontrol(ham)):
        return 0
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecisionReason": "rtk-onisle auto-rewrite",
        "updatedInput": {**veri["tool_input"], "command": yeni},
    }}, stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
