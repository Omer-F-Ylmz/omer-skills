import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import awesome_katalog as ak  # noqa: E402

ANA = """# Awesome
## Contents
- [Platforms](#platforms)

## Platforms

- [Node.js](https://github.com/sindresorhus/awesome-nodejs#readme) - Async runtime.
\t- [Cross-Platform](https://github.com/bcoe/awesome-cross-platform-nodejs#readme) - Writing cross-platform code.
- [Frontend Development](https://github.com/dypsilon/frontend-dev-bookmarks#readme)
- Linux
\t- [eBPF](https://github.com/zoidbergwill/awesome-ebpf#readme) - Tracing.
- macOS - Apple OS.
\t- [Apps](https://gitlab.com/x/awesome-mac) - Mac apps.

## Testing

- [Selenium](https://github.com/christian-bromann/awesome-selenium#readme) - Browser automation.

## Related

- [All Awesome Lists](https://github.com/topics/awesome) - Topic.
"""


def test_ana_liste_ayristir():
    s = ak.ayristir(ANA)
    assert [r[2] for r in s] == ["Node.js", "Cross-Platform", "Frontend Development", "eBPF", "Apps", "Selenium"]
    assert s[0] == ("Platforms", "", "Node.js", "sindresorhus/awesome-nodejs", "Async runtime.")
    assert s[1][1] == "Node.js"  # iç içe öğe → ebeveyn alt bölüm
    assert s[2][4] == ""  # açıklamasız
    assert s[3][1] == "Linux" and s[4][1] == "macOS"  # bağlantısız grup başlığı
    assert s[4][3] == "https://gitlab.com/x/awesome-mac"  # GitHub dışı → tam url
    assert {r[0] for r in s} == {"Platforms", "Testing"}  # Contents/Related dışarıda


ALT = """# Awesome X
Intro [badge](https://x.y).

## Contents
- [Tools](#tools)

## Tools
### Build
- [Foo](https://github.com/a/foo) - A very long description that keeps going on and on and on well past the fifteen word limit here.
* [Bar](https://bar.dev) — Bar thing.
- **[Baz](https://github.com/b/baz)**: Baz.

## License
- [CC0](https://creativecommons.org/publicdomain/zero/1.0/)
"""


def test_alt_liste_ayristir_ve_kisalt():
    s = ak.alt_ayristir(ALT)
    assert [r[0] for r in s] == ["Foo", "Bar", "Baz"]
    assert s[0][3] == "Tools / Build"
    assert len(s[0][2].split()) <= 15 and s[0][2].endswith("…")
    assert s[1] == ("Bar", "https://bar.dev", "Bar thing.", "Tools / Build")
    assert s[2][2] == "Baz."


def test_alt_liste_icerik_altinda_ve_h1_bolum():
    md = """# Awesome Y
## Contents
- [React](#react)
### React
- [Docs](https://react.dev) - Docs.
# Tools
- :free: [Tex](https://tex.example) - Textures.
# Contributing
- [Guide](https://x.y/c)
"""
    s = ak.alt_ayristir(md)
    assert [(r[0], r[3]) for r in s] == [("Docs", "Contents / React"), ("Tex", "Tools")]
