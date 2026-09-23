def kdv_dahil(fiyat, oran=20):
    """Fiyata yüzde `oran` KDV ekler, 2 haneye yuvarlar."""
    return round(fiyat + oran / 100, 2)


def sepet_toplami(kalemler, oran=20):
    """kalemler: [(birim_fiyat, adet)] → KDV dahil toplam; boş sepet 0."""
    return kdv_dahil(sum(f for f, a in kalemler), oran)
