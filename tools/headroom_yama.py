"""TOKEN-6f: Headroom 0.39.0 yaması — sıcak önbellekte frozen_message_count 0'a düşmesin.
Kök (docs/token-6f.md K2): (i) recap/away_summary yan isteği ana lineage zincirini `H + yan_user` ile ezer;
sıradaki gerçek tur `H + user` devam sayılmaz → yeni tracker → frozen 0 → kompress_background + read_maturation
tüm geçmişi yeniden yazar → sıcak önek kırılır. (iii) tracker TTL'i 600 sn sabit, CC önbelleği 1 sa.
Düzeltme: resolve_tracker yalnız son mesajı değişmiş zinciri çatal sayıp aynı tracker'a döner (frozen çatal
noktasına kısılır); is_expired max(600, isteğin önbellek TTL'i) kullanır, TTL'i handler _cc_ttl'den damgalar.
Soğuk önek (TTL üstü boşluk ya da önek değişmiş) eskisi gibi frozen 0 → sıkıştırma tetiklenir.
Idempotent: yamasız → yedek + uygula + derleme denetimi (kırıksa geri al, DUR) | yamalı → dokunmaz |
farklı sürüm ya da bilinmeyen sha → DUR, hiçbir dosyaya dokunulmaz. Etkisi proxy yeniden başlayınca.

Kullanım:
  python tools/headroom_yama.py            # uygula
  python tools/headroom_yama.py --durum    # yalnız durum
  python tools/headroom_yama.py --geri-al  # yedekten bayt-eşit geri al
"""
import argparse
import hashlib
import shutil
import sys
from pathlib import Path

KOK = Path.home() / "AppData/Local/Headroom/headroom/runtime/venv/Lib/site-packages"
SURUM = "0.39.0"

PT = "headroom/cache/prefix_tracker.py"
AN = "headroom/proxy/handlers/anthropic.py"
DUZEN = {
    PT: ("6ffca9b3da0a6a58", [
        ("        if self._cached_token_count < self.config.min_cached_tokens:\n"
         "            return 0\n"
         "        return self._cached_message_count\n",
         "        if self._cached_token_count < self.config.min_cached_tokens:\n"
         "            return 0\n"
         "        # TOKEN-6f: yan istek çatalından dönülen turda frozen çatal noktasını aşmaz\n"
         "        clamp = getattr(self, \"_fork_clamp\", None)\n"
         "        return self._cached_message_count if clamp is None else min(self._cached_message_count, clamp)\n"),
        ("        self._last_activity = time.time()\n"
         "        self._turn_number += 1\n",
         "        self._last_activity = time.time()\n"
         "        self._turn_number += 1\n"
         "        self._fork_clamp = None  # TOKEN-6f\n"),
        ("        return (time.time() - self._last_activity) > self.config.session_ttl_seconds\n",
         "        # TOKEN-6f: isteğin önbellek TTL'i (handler _cc_ttl damgası) daha uzunsa tracker onu bekler\n"
         "        ttl = max(self.config.session_ttl_seconds, getattr(self, \"_cache_ttl_hint\", 0) or 0)\n"
         "        return (time.time() - self._last_activity) > ttl\n"),
        ("        if best_key is None:\n"
         "            cap = self._default_config.max_lineages_per_session\n",
         "        if best_key is None:\n"
         "            # TOKEN-6f: yan istek çatalı (recap/away_summary, kesilen tur). Yan istek ana lineage'ın\n"
         "            # devamı olarak zinciri `H + yan_user` ile ezer; sıradaki `H + user` taze tracker (frozen 0)\n"
         "            # alırdı, oysa H önbellekte bayt bayt duruyor. Yalnız son mesajı değişmiş tek zincir kabul.\n"
         "            forks = sorted(\n"
         "                ((len(chain) - 1, key) for key, chain in by_length\n"
         "                 if self._lineage_affinities.get(key) == cache_affinity and key in self._trackers\n"
         "                 and 1 <= len(chain) - 1 < len(snap) and snap[: len(chain) - 1] == chain[:-1]),\n"
         "                reverse=True,\n"
         "            )\n"
         "            if forks and (len(forks) == 1 or forks[0][0] != forks[1][0]):\n"
         "                best_key = forks[0][1]\n"
         "                self._trackers[best_key]._fork_clamp = forks[0][0]\n"
         "        if best_key is None:\n"
         "            cap = self._default_config.max_lineages_per_session\n"),
    ]),
    AN: ("a01ca8042ad8f293", [
        ("            _cc_ttl = anthropic_cache_ttl_seconds(model, original_client_messages, system_prompt)\n",
         "            _cc_ttl = anthropic_cache_ttl_seconds(model, original_client_messages, system_prompt)\n"
         "            prefix_tracker._cache_ttl_hint = _cc_ttl or 0  # TOKEN-6f: tracker TTL'i önbellek TTL'ine bağlı\n"),
    ]),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


def _yedek(yol):
    return yol.with_name(yol.name + ".token6f-yedek")


def yamala(b, duzen):
    nl = "\r\n" if b"\r\n" in b else "\n"
    s = b.decode("utf-8")
    for eski, yeni in duzen:
        eski, yeni = eski.replace("\n", nl), yeni.replace("\n", nl)
        if s.count(eski) != 1:
            raise SystemExit(f"DUR: çapa {s.count(eski)} kez (beklenen 1): {eski.strip()[:60]}")
        s = s.replace(eski, yeni)
    return s.encode("utf-8")


def durum(kok, rel):
    orj, duzen = DUZEN[rel]
    yol, b = kok / rel, (kok / rel).read_bytes()
    if sha(b) == orj:
        return "yamasız"
    y = _yedek(yol)
    if y.exists() and sha(y.read_bytes()) == orj and yamala(y.read_bytes(), duzen) == b:
        return "yamalı"
    return f"bilinmeyen sha {sha(b)}"


def _surum(kok):
    if not (kok / f"headroom_ai-{SURUM}.dist-info").is_dir():
        bulunan = sorted(p.name for p in kok.glob("headroom_ai-*.dist-info"))
        raise SystemExit(f"DUR: Headroom {SURUM} değil ({bulunan or 'yok'}) — {kok}")


def _denetle(kok):
    hatali = []
    for rel in DUZEN:
        try:
            compile((kok / rel).read_bytes(), rel, "exec")
        except SyntaxError:
            hatali.append(rel)
    return hatali


def uygula(kok=KOK):
    _surum(kok)
    d = {rel: durum(kok, rel) for rel in DUZEN}
    if any(v not in ("yamasız", "yamalı") for v in d.values()):
        raise SystemExit(f"DUR: {d}")
    yeni = {rel: yamala((kok / rel).read_bytes(), DUZEN[rel][1]) for rel in DUZEN if d[rel] == "yamasız"}
    for rel, b in yeni.items():
        shutil.copy2(kok / rel, _yedek(kok / rel))
        (kok / rel).write_bytes(b)
    if hatali := _denetle(kok):
        for rel in yeni:
            shutil.copy2(_yedek(kok / rel), kok / rel)
        raise SystemExit(f"DUR: derleme kırık {hatali} → geri alındı")
    return {rel: "uygulandı" if rel in yeni else "yamalı: dokunulmadı" for rel in DUZEN}


def geri(kok=KOK):
    _surum(kok)
    d = {rel: durum(kok, rel) for rel in DUZEN}
    if any(v not in ("yamasız", "yamalı") for v in d.values()):
        raise SystemExit(f"DUR: {d}")
    for rel in DUZEN:
        if d[rel] == "yamalı":
            shutil.copy2(_yedek(kok / rel), kok / rel)
    return {rel: "geri alındı" if d[rel] == "yamalı" else "zaten yamasız: dokunulmadı" for rel in DUZEN}


def main(a=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--kok", type=Path, default=KOK)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--durum", action="store_true")
    g.add_argument("--geri-al", action="store_true")
    x = p.parse_args(a)
    sys.stdout.reconfigure(encoding="utf-8")
    if x.durum:
        _surum(x.kok)
        sonuc = {rel: durum(x.kok, rel) for rel in DUZEN}
    else:
        sonuc = geri(x.kok) if x.geri_al else uygula(x.kok)
    for rel, v in sonuc.items():
        print(f"{rel}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
