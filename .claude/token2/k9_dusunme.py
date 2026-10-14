"""K9: dökümlerde istek başı çıktı (düşünme dahil) dağılımı — MAX_THINKING_TOKENS tavanı neyi keser?
Düşünme tahmini = output_tokens - görünür (metin + tool_use girdisi) karakter/4. Kullanım: python k9_dusunme.py <proje_dizin_deseni>...
"""
import glob, json, os, sys

TAVANLAR = (4000, 10000, 16000)


def istekler(desenler):
    for d in desenler:
        for f in glob.glob(os.path.expanduser(f"~/.claude/projects/{d}/*.jsonl")):
            son = {}
            for satir in open(f, encoding="utf-8", errors="replace"):
                try:
                    o = json.loads(satir)
                except ValueError:
                    continue
                m = o.get("message") or {}
                if o.get("type") != "assistant" or not m.get("usage"):
                    continue
                k = son.setdefault(m.get("id") or id(o), {"out": 0, "gor": 0, "dus": False})
                k["out"] = m["usage"].get("output_tokens", 0)
                for c in m.get("content") or []:
                    t = c.get("type")
                    if t == "text":
                        k["gor"] += len(c.get("text", ""))
                    elif t == "tool_use":
                        k["gor"] += len(json.dumps(c.get("input", {}), ensure_ascii=False))
                    elif t in ("thinking", "redacted_thinking"):
                        k["dus"] = True
            yield from son.values()


def main(desenler):
    r = list(istekler(desenler))
    out = sum(x["out"] for x in r)
    dus = [max(0, x["out"] - x["gor"] // 4) for x in r]
    print(f"istek {len(r)} · çıktı {out} · düşünme~ {sum(dus)} (%{100*sum(dus)/max(out,1):.0f}) · düşünme bloklu istek {sum(x['dus'] for x in r)}")
    for t in TAVANLAR:
        asan = [d for d in dus if d > t]
        print(f"  tavan {t}: aşan istek {len(asan)} (%{100*len(asan)/max(len(r),1):.1f}) · kesilecek~ {sum(d-t for d in asan)} jeton (çıktının %{100*sum(d-t for d in asan)/max(out,1):.1f})")
    s = sorted(dus)
    if s:
        print(f"  düşünme~ p50 {s[len(s)//2]} p90 {s[int(len(s)*.9)]} p99 {s[int(len(s)*.99)]} max {s[-1]}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["C--Users-pc-Desktop-TELVE*"])
