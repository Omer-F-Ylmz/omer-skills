from fiyat import kdv_dahil, sepet_toplami


def test_kdv():
    assert kdv_dahil(100) == 120
    assert kdv_dahil(50, 10) == 55


def test_sepet():
    assert sepet_toplami([(10, 3), (5, 2)]) == 48
    assert sepet_toplami([]) == 0
