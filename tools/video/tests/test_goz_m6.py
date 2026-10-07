"""VİDEO-GÖZ-1b-1 M6 düzeltmeleri: Groq isteği Python-urllib UA'sıyla gitmez (Cloudflare 1010 → 403) · kapsam (c) mevcut eşleşmeleri korur."""
import urllib.request

from video import cli


def test_http_user_agent_urllib_degil(monkeypatch):
    gor = {}

    class Yanit:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"{}"

    def urlopen(istek, timeout):
        gor.update({k.lower(): v for k, v in istek.header_items()})
        return Yanit()
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    assert cli._http("https://api.groq.com/x", b"", {"Authorization": "Bearer k"}) == b"{}"
    assert "user-agent" in gor and "python-urllib" not in gor["user-agent"].lower() and gor["authorization"] == "Bearer k"


def test_kapsam_ek_mevcut_eslesmeyi_korur_altin_adini_ekler(tmp_path, capsys):
    p = tmp_path / "paket.md"
    p.write_text("# x\n## Segmentler\n[0:01] Zorbexx aracı\n## Sözlük eşleşmeleri\nTopview · yorum · -\n## Kareler\n", encoding="utf-8")
    (tmp_path / "a.json").write_text('{"adaylar": [{"ad": "Topview", "kaynak": "yorum"}, {"ad": "Zorbex Studio", "alias": ["Zorbex"], "kaynak": "ses"}]}',
                                     encoding="utf-8")
    assert cli.main(["altin", "kapsam", str(p), str(tmp_path / "a.json"), "--sozluk", "ek"], env={}) == 0
    assert "aday 2/2" in capsys.readouterr().out
