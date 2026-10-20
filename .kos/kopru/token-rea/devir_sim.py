"""Erken devir A/B — YALNIZ token tarafı simülasyonu (kalite ölçülmez, ayrı canlı A/B gerekir).
Son 14 gün ana-zincir oturumlarının tur başı bağlam boyundan (usage: input+cache_read+cache_creation): A = olduğu gibi,
B = bağlam >EŞIK'e çıkınca dalga.md devri + /clear: bağlam TABAN'a düşer (CC sabit bağlam + devir notu), sonraki artışlar aynı kalır.
Ağırlıklı maliyet = 1.0·input + 1.25·cache_creation + 0.1·cache_read + 5·output (girdi birimi). Devir bedeli: bir kez TABAN kadar cache yazımı + DEVIR_CIKTI çıktı jetonu."""
import glob, json, os, sys, time

EŞIK, TABAN, DEVIR_CIKTI, GUN = 120_000, 30_000, 3_000, 14


def oturum(f):
    T, gor = [], set()
    for l in open(f, encoding="utf-8", errors="replace"):
        if '"usage"' not in l: continue
        try: d = json.loads(l)
        except ValueError: continue
        m = d.get("message", {})
        u = m.get("usage")
        if d.get("type") != "assistant" or d.get("isSidechain") or not u or m.get("id") in gor: continue
        gor.add(m.get("id"))
        T.append((u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0)))
    return T


def maliyet(T, devir):
    top, ofs, n, onceki, onceki_ham = 0.0, 0, 0, 0, 0
    for i_, cc, cr, o in T:
        ctx = ham = i_ + cc + cr
        if ham < 0.7 * onceki_ham: ofs = 0  # gerçek bağlam düştü (compact/clear): kayma sıfırlanır
        onceki_ham = ham
        if devir and ctx - ofs > EŞIK:
            ofs = ctx - TABAN; n += 1; ctx = TABAN
            top += 5 * DEVIR_CIKTI  # devir notu çıktısı; yeni bağlam aşağıda tam yazılır
        else: ctx -= ofs
        # önbellek: önceki bağlam okunur, artış yazılır; bağlam küçüldüyse (devir/compact) baştan yazılır
        yeni, okuma = (ctx - onceki, onceki) if ctx > onceki else (ctx, 0)
        top += 1.25 * yeni + 0.1 * okuma + 5 * o
        onceki = ctx
    return top, n


if __name__ == "__main__":
    simdi, A, B, ns, uzun = time.time(), 0.0, 0.0, 0, 0
    for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        if simdi - os.path.getmtime(f) > GUN * 86400: continue
        T = oturum(f)
        if not T or max(i + c + r for i, c, r, _ in T) <= EŞIK: continue
        a, _ = maliyet(T, False); b, n = maliyet(T, True)
        A += a; B += b; ns += n; uzun += 1
    print(json.dumps(dict(uzun_oturum=uzun, devir_sayisi=ns, A_agirlikli_M=round(A / 1e6, 1), B_agirlikli_M=round(B / 1e6, 1), tasarruf_yuzde=round(100 * (A - B) / A, 1) if A else 0)))
