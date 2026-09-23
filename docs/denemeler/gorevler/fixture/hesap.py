def indirimli_toplam(kalemler, kupon=None, esik=500):
    """kalemler: [(birim_fiyat, adet)]; kupon: yüzde (0-100)."""
    toplam = sum(f * a for f, a in kalemler)
    if kupon:
        toplam -= toplam * kupon / 100
    if toplam > esik:
        toplam -= 50
    return round(toplam, 2)
