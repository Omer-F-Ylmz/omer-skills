"""komut.doldur: komutu "belirsiz" kartın komutu kaynaktaki birebir satırdan (betik) doldurulur."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from komut import doldur  # noqa: E402


def kart(komut="belirsiz — kaynakta yok"):
    return {"komut": komut, "alinti": {"komut": ""}}


def test_skill_frontmatter_name():
    r = doldur(kart(), "---\nname: subagent-driven-development\ndescription: x\n---\nGövde")
    assert r["komut"] == "name: subagent-driven-development" and r["alinti"]["komut"] == r["komut"]


def test_mcp_command_oncelikli_url_sonra():
    assert doldur(kart(), '{\n "command": "npx",\n "url": "http://x"\n}')["komut"] == '"command": "npx",'
    assert doldur(kart(), '{\n "type": "http",\n "url": "http://127.0.0.1:47800/servers/c/mcp"\n}')["komut"].startswith('"url"')


def test_usage_ve_plugin_adi():
    assert doldur(kart(), "Options:\nUsage: skill-ui [opts]\n")["komut"] == "Usage: skill-ui [opts]"
    assert doldur(kart(), '{\n  "name": "codex",\n}')["komut"] == '"name": "codex",'


def test_kaynakta_yoksa_belirsiz_kalir_ve_dolu_komut_degismez():
    assert doldur(kart(), "düz metin")["komut"].startswith("belirsiz")
    assert doldur(kart("git status"), "name: x")["komut"] == "git status"


def test_kisa_satirda_alinti_sonraki_satirla_uzar():
    r = doldur(kart(), "---\nname: sdp\ndescription: uzun açıklama\n---")
    assert r["komut"] == "name: sdp" and r["alinti"]["komut"] == "name: sdp\ndescription: uzun açıklama"
