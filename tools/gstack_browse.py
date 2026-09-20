#!/usr/bin/env python3
"""gstack $B (browse) yerine gecen claude.ai shim'i -- Python 3 + playwright.

Ayni dosya hem istemci hem sunucu. Ilk cagri arka planda tek bir tarayici
sunucusu baslatir; sayfa durumu cagrilar arasinda korunur, 15 dk boslukta kapanir.
Kapsam disi komutlar "claude.ai'de desteklenmez" basip exit 2 doner.
"""
import difflib
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

BOSTA_SN = 15 * 60
KAPSAM = (
    "goto snapshot click fill press text js eval console screenshot wait viewport "
    "reload back url links html status closetab pdf responsive perf stop"
).split()
# Yol argumani alan komutlar: istemci tarafinda mutlaklastirilir (sunucunun cwd'si farkli).
# Argumansiz cagride de mutlaklasir, yoksa dosya sunucunun cwd'sine duser.
YOL_ALAN = {"screenshot": "screenshot.png", "pdf": "sayfa.pdf", "responsive": "responsive"}
# snapshot bayraklari: bilinmeyen bayrak sessizce yutulmaz, exit 2 doner
SNAPSHOT_BAYRAK = {"-i", "-a", "-o", "-D"}
ZAMAN_ASIMI = float(os.environ.get("GSTACK_BROWSE_TIMEOUT") or 300)

SNAPSHOT_JS = r"""(ayar) => {
  const etk = 'a,button,input,select,textarea,[role=button],[role=link],[onclick],[contenteditable=true]';
  const sec = ayar.yalniz ? etk : etk + ',h1,h2,h3,h4,h5,h6,p,li,img,label';
  document.querySelectorAll('[data-gsref]').forEach(e => e.removeAttribute('data-gsref'));
  const cikti = []; let n = 0;
  for (const el of document.querySelectorAll(sec)) {
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) continue;
    n += 1;
    const ref = 'e' + n;
    el.setAttribute('data-gsref', ref);   // her snapshot isaretler: sonraki click calissin
    const ham = el.getAttribute('aria-label') || el.getAttribute('placeholder') ||
                el.value || el.innerText || el.id || '';
    const etiket = String(ham).replace(/\s+/g, ' ').trim().slice(0, 80);
    cikti.push('@' + ref + ' ' + el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
               ' "' + etiket + '"');
  }
  return cikti.join('\n');
}"""

OVERLAY_JS = r"""() => {
  document.querySelectorAll('[data-gsoverlay]').forEach(e => e.remove());
  for (const el of document.querySelectorAll('[data-gsref]')) {
    const r = el.getBoundingClientRect();
    const kutu = document.createElement('div');
    kutu.setAttribute('data-gsoverlay', '1');
    kutu.style.cssText = 'position:absolute;z-index:2147483647;pointer-events:none;' +
      'border:2px solid #e11;left:' + (r.left + scrollX) + 'px;top:' + (r.top + scrollY) +
      'px;width:' + r.width + 'px;height:' + r.height + 'px;';
    const etiket = document.createElement('span');
    etiket.textContent = '@' + el.getAttribute('data-gsref');
    etiket.style.cssText = 'position:absolute;left:0;top:-13px;background:#e11;color:#fff;' +
      'font:11px monospace;padding:0 3px;';
    kutu.appendChild(etiket);
    document.body.appendChild(kutu);
  }
  return document.querySelectorAll('[data-gsoverlay]').length;
}"""

OVERLAY_SIL_JS = r"""() => {
  document.querySelectorAll('[data-gsoverlay]').forEach(e => e.remove());
  return document.querySelectorAll('[data-gsoverlay]').length;
}"""

PERF_JS = """() => {
  const n = performance.getEntriesByType('navigation')[0];
  return n ? {dom: Math.round(n.domContentLoadedEventEnd),
              load: Math.round(n.loadEventEnd), tip: n.type} : {};
}"""


def ev_dizini():
    d = Path(os.environ.get("GSTACK_BROWSE_HOME") or (Path.home() / ".gstack"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def unix_soket_var():
    return hasattr(socket, "AF_UNIX") and os.name != "nt"


# --------------------------------------------------------------------------- sunucu

def _viewport_boyut(args):
    """`375x812` ve `375 812` ayni kapiya cikar; gecersiz girdi tek satir hata."""
    parca = args[0].lower().split("x") if len(args) == 1 else args[:2]
    try:
        genislik, yukseklik = (int(p) for p in parca)
    except (TypeError, ValueError):
        raise ValueError("viewport: `375x812` ya da `375 812` bekleniyor")
    return genislik, yukseklik


class Oturum:
    """Tek tarayici + tek sayfa; komutlari calistirir."""

    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.pw = sync_playwright().start()
        self.tarayici = self.pw.chromium.launch()
        self.baglam = self.tarayici.new_context()
        self.sayfa = self.baglam.new_page()
        self.konsol = []
        self.son_snapshot = {}
        self._konsol_bagla()

    def _konsol_bagla(self):
        self.sayfa.on("console", lambda m: self.konsol.append(m.type + ": " + m.text))

    def _hedef(self, secici):
        if secici.startswith("@"):
            hedef = self.sayfa.locator('[data-gsref="' + secici[1:] + '"]')
            if hedef.count() == 0:      # beklemeden bildir; 30 sn timeout yerine
                raise ValueError(secici + " yok -- once snapshot -i")
            return hedef
        return self.sayfa.locator(secici)

    def _snapshot(self, args):
        """Her cagri isaretler; -i listeyi daraltir, -D fark verir, -a PNG yazar."""
        kapsam = "dar" if "-i" in args else "tam"   # ref numaralari kapsama gore kayar
        liste = self.sayfa.evaluate(SNAPSHOT_JS, {"yalniz": kapsam == "dar"})
        cikti = liste
        if "-D" in args:
            onceki = self.son_snapshot.get(kapsam)
            if onceki is None:
                cikti = "(onceki snapshot yok)\n" + liste
            elif onceki == liste:
                cikti = "(fark yok)"
            else:
                cikti = "\n".join(difflib.unified_diff(
                    onceki.split("\n"), liste.split("\n"), "onceki", "simdi", lineterm=""))
        self.son_snapshot[kapsam] = liste
        if "-a" in args:
            yol = args[args.index("-o") + 1] if "-o" in args else "annotated.png"
            self.sayfa.evaluate(OVERLAY_JS)
            try:
                self.sayfa.screenshot(path=yol, full_page=True)
            finally:
                self.sayfa.evaluate(OVERLAY_SIL_JS)
            cikti = cikti + "\n" + yol
        return cikti

    def calistir(self, komut, args):
        s = self.sayfa
        if komut == "goto":
            self.konsol.clear()
            s.goto(args[0], wait_until="load")
            return s.url
        if komut == "url":
            return s.url
        if komut == "text":
            return s.inner_text("body")
        if komut == "html":
            return s.content()
        if komut == "snapshot":
            return self._snapshot(args)
        if komut == "click":
            self._hedef(args[0]).click()
            return "tiklandi: " + args[0]
        if komut == "fill":
            self._hedef(args[0]).fill(args[1] if len(args) > 1 else "")
            return "dolduruldu: " + args[0]
        if komut == "press":
            if len(args) > 1:
                self._hedef(args[0]).press(args[1])
            else:
                s.keyboard.press(args[0])
            return "basildi: " + args[-1]
        if komut in ("js", "eval"):
            return json.dumps(s.evaluate(args[0]), ensure_ascii=False)
        if komut == "console":
            return "\n".join(self.konsol) or "(konsol bos)"
        if komut == "screenshot":
            hedef = args[0] if args else "screenshot.png"
            s.screenshot(path=hedef, full_page=True)
            return hedef
        if komut == "pdf":
            hedef = args[0] if args else "sayfa.pdf"
            s.pdf(path=hedef)
            return hedef
        if komut == "wait":
            if args and args[0].isdigit():
                s.wait_for_timeout(int(args[0]))
            elif args:
                s.wait_for_selector(args[0])
            else:
                s.wait_for_load_state("networkidle")
            return "beklendi"
        if komut == "viewport":
            genislik, yukseklik = _viewport_boyut(args)
            s.set_viewport_size({"width": genislik, "height": yukseklik})
            return "viewport: %dx%d" % (genislik, yukseklik)
        if komut == "reload":
            s.reload(wait_until="load")
            return s.url
        if komut == "back":
            s.go_back()
            return s.url
        if komut == "links":
            baglar = s.eval_on_selector_all(
                "a[href]", "es => es.map(e => e.href + ' :: ' + e.innerText.trim())")
            return "\n".join(baglar) or "(bag yok)"
        if komut == "responsive":
            onek = args[0] if args else "responsive"
            yollar = []
            for g in (390, 768, 1440):
                s.set_viewport_size({"width": g, "height": 900})
                p = onek + "-" + str(g) + ".png"
                s.screenshot(path=p, full_page=True)
                yollar.append(p)
            return "\n".join(yollar)
        if komut == "perf":
            return json.dumps(s.evaluate(PERF_JS), ensure_ascii=False)
        if komut == "status":
            return "url: %s\nkonsol: %d mesaj\ntarayici: chromium (headless)" % (
                s.url, len(self.konsol))
        if komut == "closetab":
            self.sayfa.close()
            self.sayfa = self.baglam.new_page()
            self.konsol = []
            self._konsol_bagla()
            return "sekme kapatildi"
        raise ValueError(komut)

    def kapat(self):
        for f in (self.baglam.close, self.tarayici.close, self.pw.stop):
            try:
                f()
            except Exception:
                pass


def _satir_oku(baglanti):
    ham = b""
    while not ham.endswith(b"\n"):
        parca = baglanti.recv(65536)
        if not parca:
            break
        ham += parca
    return ham


def _adres_sil(d):
    try:
        (d / ("browse.sock" if unix_soket_var() else "browse.port")).unlink()
    except OSError:
        pass


def sunucu():
    d = ev_dizini()
    if unix_soket_var():
        yol = d / "browse.sock"
        if yol.exists():
            yol.unlink()
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(str(yol))
    else:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind(("127.0.0.1", 0))
        gecici = d / "browse.port.tmp"
        gecici.write_text(str(srv.getsockname()[1]), encoding="utf-8")
        os.replace(str(gecici), str(d / "browse.port"))
    srv.listen(8)
    srv.settimeout(30)

    oturum = Oturum()
    son = time.time()
    try:
        while True:
            try:
                baglanti, _ = srv.accept()
            except socket.timeout:
                if time.time() - son > BOSTA_SN:
                    return
                continue
            son = time.time()
            with baglanti:
                ham = _satir_oku(baglanti)
                if not ham.strip():
                    continue
                istek = json.loads(ham.decode("utf-8"))
                if istek["cmd"] == "stop":
                    baglanti.sendall(json.dumps(
                        {"code": 0, "out": "sunucu kapatildi", "err": ""}).encode("utf-8") + b"\n")
                    # once dinleyici + adres: hemen gelen komut bayat sokete baglanmasin
                    srv.close()
                    _adres_sil(d)
                    return
                try:
                    yanit = {"code": 0, "out": str(oturum.calistir(istek["cmd"], istek["args"])),
                             "err": ""}
                except Exception as hata:
                    yanit = {"code": 1, "out": "",
                             "err": type(hata).__name__ + ": " + str(hata)}
                baglanti.sendall(json.dumps(yanit, ensure_ascii=False).encode("utf-8") + b"\n")
    finally:
        try:
            srv.close()
        except OSError:
            pass
        _adres_sil(d)
        oturum.kapat()


# --------------------------------------------------------------------------- istemci

def baglan(d):
    if unix_soket_var():
        yol = d / "browse.sock"
        if not yol.exists():
            return None
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        hedef = str(yol)
    else:
        p = d / "browse.port"
        if not p.exists():
            return None
        try:
            hedef = ("127.0.0.1", int(p.read_text(encoding="utf-8").strip()))
        except (OSError, ValueError):
            return None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(ZAMAN_ASIMI)
    try:
        s.connect(hedef)
        return s
    except OSError:
        s.close()
        return None


def sunucu_baslat(d):
    """Yarisi onlemek icin O_EXCL kilidi; bayat kilit 90 sn sonra devralinir."""
    kilit = d / "browse.lock"
    try:
        os.close(os.open(str(kilit), os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        if time.time() - kilit.stat().st_mtime < 90:
            return
        kilit.touch()
    ek = {}
    if os.name == "nt":
        ek["creationflags"] = 0x00000008 | 0x00000200  # DETACHED_PROCESS | NEW_PROCESS_GROUP
    else:
        ek["start_new_session"] = True
    subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), "--serve"],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        env=os.environ, **ek)


def _sunucu_ac(d):
    sunucu_baslat(d)
    baglanti, bitis = None, time.time() + 120
    while baglanti is None and time.time() < bitis:
        time.sleep(0.3)
        baglanti = baglan(d)
    try:
        (d / "browse.lock").unlink()
    except OSError:
        pass
    return baglanti


def _gonder(baglanti, komut, args):
    """Yanit satirini dondurur; sunucu olmusse None (zaman asimi yukari cikar)."""
    try:
        with baglanti:
            baglanti.sendall(json.dumps(
                {"cmd": komut, "args": args}, ensure_ascii=False).encode("utf-8") + b"\n")
            ham = _satir_oku(baglanti)
    except (ConnectionResetError, ConnectionRefusedError, BrokenPipeError):
        return None                      # kapanmakta olan sunucu; traceback basma
    return ham if ham.strip() else None


def istemci(komut, args):
    d = ev_dizini()
    ham = None
    for ikinci in (False, True):
        baglanti = baglan(d)
        if baglanti is None:
            if komut == "stop":
                print("sunucu zaten kapali")
                return 0
            baglanti = _sunucu_ac(d)
            if baglanti is None:
                sys.stderr.write("browse: tarayici sunucusu baslatilamadi\n")
                return 1
        try:
            ham = _gonder(baglanti, komut, args)
        except socket.timeout:
            # yavas komut: sunucu yasiyor, yeniden baslatmak komutu iki kez kosturur
            sys.stderr.write("browse: sunucu %g sn icinde yanit vermedi\n" % ZAMAN_ASIMI)
            return 1
        if ham is not None:
            break
        if ikinci:
            sys.stderr.write("browse: sunucudan yanit gelmedi\n")
            return 1
        _adres_sil(d)                    # bayat adres; sunucuyu bir kez yeniden baslat
    yanit = json.loads(ham.decode("utf-8"))
    if yanit["out"]:
        print(yanit["out"])
    if yanit["err"]:
        sys.stderr.write(yanit["err"] + "\n")
    return yanit["code"]


def main(argv):
    if argv and argv[0] == "--serve":
        sunucu()
        return 0
    if not argv:
        sys.stderr.write("kullanim: browse <komut> [arg...]\nkapsam: " + " ".join(KAPSAM) + "\n")
        return 2
    komut, args = argv[0], list(argv[1:])
    if komut not in KAPSAM:
        sys.stderr.write(
            "browse: '" + komut + "' claude.ai'de desteklenmez (kapsam disi).\n"
            "Desteklenen komutlar: " + " ".join(KAPSAM) + "\n")
        return 2
    if komut in YOL_ALAN:
        args[0:1] = [os.path.abspath(args[0] if args else YOL_ALAN[komut])]
    if komut == "snapshot":
        bilinmeyen = [a for a in args if a.startswith("-") and a not in SNAPSHOT_BAYRAK]
        if bilinmeyen:
            sys.stderr.write(
                "browse: snapshot bayragi desteklenmez: " + bilinmeyen[0] + "\n"
                "Desteklenen: -i (yalniz etkilesimli) -a (isaretli PNG) "
                "-o <yol> -D (onceki snapshot ile fark)\n")
            return 2
        if "-o" in args:
            i = args.index("-o") + 1
            if i >= len(args) or "-a" not in args:
                sys.stderr.write("browse: -o bir yol bekler ve yalniz -a ile kullanilir\n")
                return 2
            args[i] = os.path.abspath(args[i])
        elif "-a" in args:
            args += ["-o", os.path.abspath("annotated.png")]
    return istemci(komut, args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
