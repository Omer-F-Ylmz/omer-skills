import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import aciklama_yaz as ay  # noqa: E402


def test_json_dizi_citli_yanit():
    assert ay.json_dizi('Tamam:\n```json\n[{"ad": "x", "aciklama": "Use when y."}]\n```') == [{"ad": "x", "aciklama": "Use when y."}]
    assert ay.json_dizi("yanıt yok") == []


def test_gecerli_tetik_tavan_degisim():
    assert ay.gecerli("Does x.", "Does x. Use when the user asks for x.")
    assert not ay.gecerli("Does x.", "Does x.")  # tetik yok + değişmedi
    assert not ay.gecerli("", "Use when " + "a" * 1100)  # tavan
    assert ay.gecerli("PDF birleştirir.", "PDF birleştirir. PDF birleştirme istendiğinde kullan.")


def test_hedefler_tekil(tmp_path):
    s = tmp_path / "a" / "SKILL.md"
    s.parent.mkdir()
    s.write_text("---\nname: a\ndescription: Kısa.\n---\n" + "\n".join(f"satır {i}" for i in range(100)), encoding="utf-8")
    tsv = tmp_path / "d.tsv"
    bas = "ad\tkaynak\taile\tyol\tsorunlar\n"
    tsv.write_text(bas + f"a\tplugin\tx\t{s.parent}\ttetik_yok\na\tgevşek\ty\t{s}\ttetik_yok\nb\tplugin\tx\t{s}\tcift\n", encoding="utf-8")
    h = ay.hedefler(tsv)
    assert len(h) == 1 and h[0]["aciklama"] == "Kısa." and h[0]["govde"].count("\n") == 59
