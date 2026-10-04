"""KÜÇÜK-1 K3: parti baslat hedefsiz → docs/video-tarama/kuyruk.md (kuyruk eylemi gibi); traceback yok."""
from test_m2a import V, Sahte, _ctx, _kurulum, _ns

from video import parti as pt


def test_baslat_hedefsiz_varsayilan_kuyruk(tmp_path):
    kok = _kurulum(tmp_path, [V[0]])
    varsayilan = kok / "docs" / "video-tarama" / "kuyruk.md"
    varsayilan.parent.mkdir(parents=True, exist_ok=True)
    (kok / "kuyruk.md").replace(varsayilan)
    ns = _ns("baslat", None)
    ns.hedef = None  # _ns hedefi str()'liyor ("None"); argparse hedefsizde None verir
    assert pt.parti(ns, _ctx(kok, Sahte())) == 0
