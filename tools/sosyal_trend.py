"""Günlük yükselen ücretsiz AI araçları -> sosyal-oto konu kuyruğu (0 token, model yok, API anahtarı yok).
Kaynaklar: HF Spaces trendingScore · GitHub (OSI lisanslı, yeni, yıldız) · HN Show HN · YouTube arama (yalnız talep sinyali).
Kullanım: python tools/sosyal_trend.py [--n 10]   (curl kullanır: Windows sertifika deposu; urllib bazı uçlarda CERTIFICATE_VERIFY_FAILED)
Çıktı: sosyal-oto\\buyume\\trend-<tarih>.md + konu-kuyrugu.json (hat.py a <url> girdisi: url, ad, kaynak, metrik, ucretsiz_kanit)"""
import json, os, re, subprocess, sys, time
from pathlib import Path

DIZ = Path.home() / "Desktop" / "Claude ile yapılanlar" / "sosyal-oto" / "buyume"
KUYRUK = DIZ / "konu-kuyrugu.json"
YASAK = re.compile(r"uncensor|nsfw|porn|nude|undress|jailbreak|crack|keygen|deepfake|hentai|erotic|sexy|waifu|gamble|casino|face.?swap|bw*777w*b|slot|betb", re.I)
OSI = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-3.0", "Unlicense"}
NOWIN = 0x08000000 if sys.platform == "win32" else 0


def _curl(url, saniye=30):
    p = subprocess.run(["curl", "-s", "-L", "-m", str(saniye), "-A", "sosyal-trend/1", url], capture_output=True,
                       encoding="utf-8", errors="replace", env=os.environ.copy(), creationflags=NOWIN)
    return p.stdout


def _json(url):
    try:
        return json.loads(_curl(url))
    except ValueError:
        return None


def _http_ok(url):
    p = subprocess.run(["curl", "-s", "-L", "-m", "20", "-o", os.devnull, "-w", "%{http_code}", "-A", "Mozilla/5.0", url],
                       capture_output=True, encoding="utf-8", env=os.environ.copy(), creationflags=NOWIN)
    return p.stdout.strip().startswith(("2", "3"))


def hf(n):
    for s in _json("https://huggingface.co/api/spaces?sort=trendingScore&limit=60&full=true") or []:
        ad, kisa = s["id"], (s.get("cardData") or {}).get("short_description") or ""
        if YASAK.search(ad + kisa) or s.get("private"):
            continue
        yield {"ad": ad.split("/")[1], "url": f"https://huggingface.co/spaces/{ad}", "kaynak": "hf-spaces", "skor": s.get("trendingScore", 0),
               "metrik": f"trendingScore {s.get('trendingScore')}, {s.get('likes')} beğeni", "aciklama": kisa,
               "ucretsiz_kanit": "herkese açık HF Space (tarayıcıda hesapsız çalışır; ZeroGPU kotası olabilir)"}


def gh(n):
    t = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 14 * 86400))
    d = _json(f"https://api.github.com/search/repositories?q=topic:ai+created:>{t}+stars:>150&sort=stars&per_page=30") or {}
    for r in d.get("items", []):
        lic = (r.get("license") or {}).get("spdx_id")
        if lic not in OSI or YASAK.search(r["full_name"] + (r.get("description") or "")):
            continue
        yield {"ad": r["name"], "url": r.get("homepage") or r["html_url"], "kaynak": "github", "skor": r["stargazers_count"],
               "metrik": f"{r['stargazers_count']} yıldız, oluşturulma {r['created_at'][:10]}", "aciklama": r.get("description") or "",
               "ucretsiz_kanit": f"açık kaynak lisans {lic}: {r['html_url']}"}


def hn(n):
    t = int(time.time()) - 7 * 86400
    d = _json(f"https://hn.algolia.com/api/v1/search?tags=show_hn&query=free%20AI%20tool&numericFilters=created_at_i>{t},points>20&hitsPerPage=20") or {}
    for h in d.get("hits", []):
        if h.get("url") and not YASAK.search(h["title"]):
            yield {"ad": re.sub(r"^Show HN:\s*", "", h["title"])[:70], "url": h["url"], "kaynak": "hn-show", "skor": h["points"],
                   "metrik": f"{h['points']} puan, {h.get('num_comments', 0)} yorum", "aciklama": h["title"],
                   "ucretsiz_kanit": f"sayfada 'free/open source' geçmeli (kontrol edilir): https://news.ycombinator.com/item?id={h['objectID']}"}


def yt_talep():
    p = subprocess.run(["yt-dlp", "-J", "--flat-playlist", "--no-warnings", "--playlist-end", "15", "https://www.youtube.com/results?search_query=free+AI+tool&sp=EgQIAxAB"], capture_output=True,
                       encoding="utf-8", errors="replace", timeout=180, env=os.environ.copy(), creationflags=NOWIN)
    try:
        e = json.loads(p.stdout)["entries"]
    except Exception:
        return []
    return sorted(({"baslik": x.get("title", ""), "izlenme": x.get("view_count") or 0, "url": x.get("url")} for x in e),
                  key=lambda x: -x["izlenme"])[:5]


def main(n=10):
    DIZ.mkdir(parents=True, exist_ok=True)
    kuyruk = json.loads(KUYRUK.read_text(encoding="utf-8")) if KUYRUK.exists() else []
    var = {k["url"] for k in kuyruk}
    kaynaklar = {f.__name__: sorted(f(n), key=lambda x: -x["skor"]) for f in (hf, gh, hn)}
    sira = [x for grup in zip(*[(v + [None] * n)[:n] for v in kaynaklar.values()]) for x in grup if x]  # kaynaklar arası dönüşümlü
    yeni, elenen = [], []
    for x in sira:
        if x["url"] in var or len(yeni) >= n:
            continue
        if not _http_ok(x["url"]):
            elenen.append((x["ad"], "URL açılmıyor")); continue
        if x["kaynak"] == "hn-show" and not re.search(r"free|open[- ]source|ücretsiz", _curl(x["url"], 20), re.I):
            elenen.append((x["ad"], "sayfada ücretsiz/açık kaynak kanıtı yok")); continue
        x.update(tarih=time.strftime("%Y-%m-%d"), durum="yeni"); yeni.append(x); var.add(x["url"])
    KUYRUK.write_text(json.dumps(kuyruk + yeni, ensure_ascii=False, indent=1), encoding="utf-8")
    tal = yt_talep()
    md = [f"---\ntype: trend\nstatus: active\ntags: [sosyal-buyume, trend]\nrelatedTo: [SOSYAL-BUYUME-1]\n---\n# Trend {time.strftime('%Y-%m-%d')}",
          f"Kuyruğa eklenen {len(yeni)} · elenen {len(elenen)} · kaynaklar: HF Spaces API, GitHub Search API, HN Algolia, yt-dlp ytsearchdate\n"]
    md += [f"- **{x['ad']}** ({x['kaynak']}) {x['metrik']} — {x['url']}\n  - ücretsiz kanıtı: {x['ucretsiz_kanit']}" for x in yeni]
    md += ["\nElenen: " + "; ".join(f"{a} ({b})" for a, b in elenen) if elenen else "\nElenen: yok", "\nYouTube talep sinyali (rakip videolar, bu hafta 'free AI tool'):"]
    md += [f"- {t['izlenme']} izl · {t['baslik'][:80]} — {t['url']}" for t in tal] or ["- alınamadı"]
    (DIZ / f"trend-{time.strftime('%Y-%m-%d')}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"kuyruğa +{len(yeni)} (toplam {len(kuyruk) + len(yeni)}), elenen {len(elenen)}, yt talep {len(tal)}")


if __name__ == "__main__":
    sys.stdout and sys.stdout.reconfigure(encoding="utf-8")  # pythonw: stdout yok
    main(int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 10)
