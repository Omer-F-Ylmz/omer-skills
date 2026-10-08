import http.client

import pytest

from video import getir as gt


def test_bozuk_port_getir_hata():
    """YT1 5: açıklamadaki `http://x:3eee` adresi InvalidURL (ValueError) atar; paket düşmez, GetirHata olur."""
    def al(url):
        raise http.client.InvalidURL("nonnumeric port: '3eee'")
    with pytest.raises(gt.GetirHata):
        gt.getir("http://x:3eee/", al=al)
