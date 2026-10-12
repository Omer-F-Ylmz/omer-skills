"""FABLE-AJAN envanteri (salt okuma): küçük ajanlar — model, aile, satır, önsöz bloğu var mı.

Kaynaklar: ~/.claude/agents · <repo>/.claude/agents · <repo>/ajanlar/** · plugin önbelleği agents/*.md ·
tools/video içinde --model geçen satırlar. Çıktı TSV (stdout ya da --tsv yol); özet stderr'e.
python tools/olcum/fable_ajan_envanter.py [--tsv yol]
"""
import collections
import pathlib
import re
import sys

KOK = pathlib.Path(__file__).resolve().parents[2]
EV = pathlib.Path.home() / ".claude"
ISARETLER = ("godmode:basla", "ders-yuvasi:basla", "calisma-protokolu")


def on_bilgi(metin):
    """Frontmatter'dan (name, model); yoksa (None, None)."""
    m = re.match(r"---\r?\n(.*?)\r?\n---", metin, re.S)
    if not m:
        return None, None
    alan = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    return alan.get("name", "").strip().strip("'\""), alan.get("model", "").strip().strip("'\"") or "inherit"


def aile(ad):
    on = ad.split("-")[0] if "-" in ad else ""
    return on if 2 <= len(on) <= 4 and on.isalpha() and on.islower() else "diger"


def ajan_satirlari():
    kaynaklar = [("cc-kullanici", EV / "agents", "*.md"), ("repo-claude", KOK / ".claude" / "agents", "*.md"),
                 ("repo-ajanlar", KOK / "ajanlar", "**/*.md"), ("plugin", EV / "plugins" / "cache", "**/agents/*.md")]
    for kaynak, kok, desen in kaynaklar:
        if not kok.is_dir():
            continue
        for yol in sorted(kok.glob(desen)):
            if yol.name.lower() in ("readme.md", "index.md"):
                continue
            metin = yol.read_text(encoding="utf-8", errors="replace")
            ad, model = on_bilgi(metin)
            if not ad:
                continue
            onsoz = ",".join(i.split(":")[0] for i in ISARETLER if i in metin) or "-"
            yield kaynak, ad, model, aile(ad), metin.count("\n") + 1, onsoz, str(yol)


def video_satirlari():
    for yol in sorted((KOK / "tools" / "video").glob("*.py")):
        for no, satir in enumerate(yol.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = re.search(r"--model[\"',\s]+[\"']?(sonnet|haiku|opus)", satir)
            if m:
                yield "video", f"{yol.stem}:{no}", m.group(1), "vid", 1, "-", str(yol)


def main(argv):
    satirlar = list(ajan_satirlari()) + list(video_satirlari())
    tsv = "kaynak\tad\tmodel\taile\tsatir\tonsoz\tyol\n" + "".join("\t".join(map(str, s)) + "\n" for s in satirlar)
    if "--tsv" in argv:
        pathlib.Path(argv[argv.index("--tsv") + 1]).write_bytes(tsv.encode("utf-8"))
    else:
        sys.stdout.write(tsv)
    say = collections.Counter((s[0], s[2]) for s in satirlar)
    print("; ".join(f"{k}/{m}={n}" for (k, m), n in sorted(say.items())), file=sys.stderr)
    kucuk = [s for s in satirlar if s[2] in ("sonnet", "haiku")]
    print("kucuk (sonnet+haiku):", len(kucuk), "aile:", dict(collections.Counter(s[3] for s in kucuk).most_common()), file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
