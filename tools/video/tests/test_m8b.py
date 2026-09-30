"""M8b: yt-dlp'ye kimlik hiçbir zaman çıplak verilmez; her zaman tam URL (tireli kimlik seçenek sanılmasın)."""
import pytest

from test_video import VID, Kos, ortam  # noqa: F401  (ortam fixture)
from video.cli import main


def _ytdlp(ortam, vid):
    kos = Kos()
    assert main(["ozet", "--", vid], env=ortam, kos=kos) == 0
    main(["kare", "--t", "0:30", "--en-fazla", "1", "--", vid], env=ortam, kos=kos)  # yalnız -g çağrısı gerekli
    return [a for a in kos.cagri if a[0] == "yt-dlp"]


@pytest.mark.parametrize("vid", ["-_S3KD0ZIfI", "-INveHwbRz4", VID])
def test_ytdlp_ciplak_kimlik_almaz_url_alir(ortam, vid):
    yt = _ytdlp(ortam, vid)
    assert any("-J" in a for a in yt) and any("--sub-langs" in a for a in yt) and any("-g" in a for a in yt)
    for a in yt:
        assert vid not in a
        assert f"https://www.youtube.com/watch?v={vid}" in a
