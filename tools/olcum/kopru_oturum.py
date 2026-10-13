"""TOKEN-9: köprü ajanı (claude -p) oturumlarının sayısal ölçümü.

Yalnız entrypoint=sdk-cli ve ilk istemde `.kos/kopru/gorev/<görev>[-dN].kilit` olan
oturumlar sayılır; etkileşimli oturumların içeriği açılmaz. Çıktı yalnız sayılardır.
Kullanım: python -I kopru_oturum.py <tsv_çıktı> [YYYY-MM-DD]   |   --test
"""
import glob, json, os, re, sys
from datetime import datetime, timedelta, timezone

KOK = os.path.expanduser("~/.claude/projects")
KILIT = re.compile(r"gorev/([a-z0-9-]+?)(?:-d(\d+))?\.kilit")
CAGRI = re.compile(r"çağrı (\d+)/45")
TR = timezone(timedelta(hours=3))
DURUM_N = 10  # ilk N API isteği = "durum çıkarma" evresi
# input fiyatına göre göreli ağırlık (cache_write 1.25x, cache_read 0.1x, output 5x)
AGIRLIK = {"inp": 1.0, "cw": 1.25, "cr": 0.1, "out": 5.0}


def metin(m):
    c = m.get("content")
    if isinstance(c, str):
        return c
    return " ".join(b.get("text", "") for b in c or [] if isinstance(b, dict))


def olc(satirlar):
    """satirlar: jsonl dict'leri. Köprü oturumu değilse None."""
    ep = next((d["entrypoint"] for d in satirlar if "entrypoint" in d), None)
    if ep != "sdk-cli":
        return None
    ilk = next((d for d in satirlar if d.get("type") == "user" and not d.get("isMeta")), None)
    m = ilk and KILIT.search(metin(ilk.get("message", {})).replace("\\", "/"))
    if not m:
        return None
    istek, sira, arac, cagri_max = {}, [], 0, 0
    for d in satirlar:
        if d.get("type") == "assistant" and not d.get("isSidechain"):
            msg = d.get("message", {})
            mid = msg.get("id")
            arac += sum(1 for b in msg.get("content") or [] if isinstance(b, dict) and b.get("type") == "tool_use")
            u = msg.get("usage")
            if mid and u and mid not in istek:
                istek[mid] = (u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0),
                              u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0), msg.get("model", ""))
                sira.append(mid)
            elif mid in istek and u:  # akış parçalarında son usage en büyük output'u taşır
                o = istek[mid]
                istek[mid] = o[:3] + (max(o[3], u.get("output_tokens", 0)), o[4])
        for x in CAGRI.findall(json.dumps(d, ensure_ascii=False)) if d.get("type") in ("attachment", "user", "system") else []:
            cagri_max = max(cagri_max, int(x))
    if not sira:
        return None
    ts = [d["timestamp"] for d in satirlar if "timestamp" in d]
    t0 = datetime.fromisoformat(ts[0].replace("Z", "+00:00")).astimezone(TR)
    t1 = datetime.fromisoformat(ts[-1].replace("Z", "+00:00")).astimezone(TR)
    v = [istek[k] for k in sira]
    top = lambda i, xs=v: sum(x[i] for x in xs)
    agir = lambda xs: sum(AGIRLIK["inp"] * x[0] + AGIRLIK["cw"] * x[1] + AGIRLIK["cr"] * x[2] + AGIRLIK["out"] * x[3] for x in xs)
    on = v[:DURUM_N]
    return {
        "gorev": m.group(1), "d": int(m.group(2) or 0), "bas": t0.strftime("%Y-%m-%d %H:%M"),
        "dk": round((t1 - t0).total_seconds() / 60, 1), "model": v[0][4].replace("claude-", ""),
        "tur": len(v), "arac": arac, "cagri_max": cagri_max,
        "inp": top(0), "cw": top(1), "cr": top(2), "out": top(3),
        "onek": sum(v[0][:3]), "son_ctx": sum(v[-1][:3]), "durum_ctx": sum(sum(x[:3]) for x in on), "durum_agir": round(agir(on)),
        "agir": round(agir(v)),
    }


def oku(yol):
    with open(yol, encoding="utf-8") as h:
        for l in h:
            try:
                yield json.loads(l)
            except ValueError:
                pass


def main(cikti, gun="2026-10-13"):
    satirlar = []
    for f in glob.glob(os.path.join(KOK, "C--Projeler-omer-skills*", "*.jsonl")):
        bas = [d for _, d in zip(range(40), oku(f))]
        if next((d["entrypoint"] for d in bas if "entrypoint" in d), None) != "sdk-cli":
            continue  # etkileşimli oturum: dosyanın geri kalanı açılmaz
        r = olc(list(oku(f)))
        if r and r["bas"].startswith(gun):
            r["oturum"] = os.path.basename(f)[:8]
            satirlar.append(r)
    satirlar.sort(key=lambda r: r["bas"])
    alan = ["bas", "gorev", "d", "oturum", "model", "dk", "tur", "arac", "cagri_max", "inp", "cw", "cr", "out",
            "onek", "son_ctx", "durum_ctx", "durum_agir", "agir"]
    with open(cikti, "w", encoding="utf-8", newline="\n") as h:
        h.write("\t".join(alan) + "\n")
        for r in satirlar:
            h.write("\t".join(str(r[a]) for a in alan) + "\n")
    print(f"{len(satirlar)} köprü oturumu -> {cikti}")


def _test():
    u = lambda i, cr, out: {"input_tokens": i, "cache_creation_input_tokens": 0, "cache_read_input_tokens": cr, "output_tokens": out}
    s = [{"entrypoint": "sdk-cli", "type": "user", "timestamp": "2026-10-13T10:00:00Z",
          "message": {"content": "X görevi. kilit: .kos\\kopru\\gorev\\x-1-d2.kilit"}},
         {"type": "assistant", "timestamp": "2026-10-13T10:01:00Z", "message": {"id": "a", "model": "claude-opus", "usage": u(5, 100, 1),
          "content": [{"type": "tool_use"}]}},
         {"type": "assistant", "timestamp": "2026-10-13T10:01:01Z", "message": {"id": "a", "usage": u(5, 100, 9), "content": [{"type": "tool_use"}]}},
         {"type": "attachment", "timestamp": "2026-10-13T10:02:00Z", "x": "çağrı 7/45"},
         {"type": "assistant", "timestamp": "2026-10-13T10:03:00Z", "message": {"id": "b", "usage": u(1, 200, 2), "content": []}}]
    r = olc(s)
    assert (r["gorev"], r["d"], r["tur"], r["arac"], r["cagri_max"]) == ("x-1", 2, 2, 2, 7), r
    assert (r["inp"], r["cr"], r["out"], r["onek"], r["dk"]) == (6, 300, 11, 105, 3.0), r
    s[0]["entrypoint"] = "cli"
    assert olc(s) is None
    print("test ok")


if __name__ == "__main__":
    _test() if sys.argv[1:] == ["--test"] else main(*sys.argv[1:])
