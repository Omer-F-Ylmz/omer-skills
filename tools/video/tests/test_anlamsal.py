"""VİDEO-AKIL-1b-2a DEVAM-1: serbest metin alanları anlamsal puan (fastembed çok dilli; gerçek model)."""
from video import altin as au


def _rapor(**bol):
    return "# b\n## Özet\nmetin\n" + "".join(f"## {k}\n{v}\n" for k, v in bol.items())


def test_turkce_altin_ayni_anlamli_ingilizce_satirla_eslesir():
    a = {"is_akisi": [{"adim": "Kullanıcı Blender'da arabanın modelini hazırlar", "zaman": "1:00", "araclar": []}]}
    r = _rapor(**{"İş akışı": "- The user prepares the car model in Blender"})
    assert au.puan(r, a)["is_akisi"] == (1, 1)  # kelime örtüşmesi: ortak kelime yok → 0


def test_baska_videonun_maddesi_eslesmez():
    a = {"is_akisi": [{"adim": "Kullanıcı Blender'da arabanın modelini hazırlar", "zaman": "1:00", "araclar": []}]}
    r = _rapor(**{"İş akışı": "- Supabase veritabanında kullanıcı tablosuna satır güvenliği politikası eklenir"})
    assert au.puan(r, a)["is_akisi"] == (0, 1)


def test_bir_rapor_satiri_iki_altin_maddeyi_karsilayamaz():
    a = {"is_akisi": [{"adim": "Blender'da araba modelini hazırla", "zaman": "1:00", "araclar": []},
                      {"adim": "Blender'da arabanın modelini kur", "zaman": "2:00", "araclar": []}]}
    r = _rapor(**{"İş akışı": "- Prepare the car model in Blender"})
    assert au.puan(r, a)["is_akisi"] == (1, 2)


def _sabit_kos(monkeypatch, kos):
    """embed'i sabitle: altın i ile satır j kosinüsü kos[i][j] (altın = birim vektör, satır = sütunlar)."""
    import numpy as np
    from video import anlamsal
    k = np.array(kos, dtype=float)
    monkeypatch.setattr(anlamsal, "embed", lambda m: np.eye(k.shape[0]) if m and m[0].startswith("a") else k.T)
    return anlamsal


def test_jev_bant_ici_cifti_yargic_karar_verir_bant_disi_kosinus(monkeypatch):
    # JEV-1-devam-2 (3): eşik 0.5; a0-s0 0.45 (bant, jev evet) · a1-s1 0.55 (bant, jev hayır) · a2-s2 0.9 (bant dışı, jev'e gitmez)
    an = _sabit_kos(monkeypatch, [[0.45, 0, 0], [0, 0.55, 0], [0, 0, 0.9]])
    sorulan = []
    def yargic(ciftler):
        sorulan.extend(ciftler)
        return [a == "a0" for a, _ in ciftler]
    es = an.esle(["a0", "a1", "a2"], ["s0", "s1", "s2"], 0.5, yargic=yargic)
    assert sorted((i, j) for i, j, _ in es) == [(0, 0), (2, 2)]
    assert sorted(sorulan) == [("a0", "s0"), ("a1", "s1")]


def test_jev_yargic_yoksa_ya_da_hata_verirse_kosinus(monkeypatch):
    an = _sabit_kos(monkeypatch, [[0.45, 0], [0, 0.55]])
    assert [(i, j) for i, j, _ in an.esle(["a0", "a1"], ["s0", "s1"], 0.5)] == [(1, 1)]
    assert [(i, j) for i, j, _ in an.esle(["a0", "a1"], ["s0", "s1"], 0.5, yargic=lambda c: None)] == [(1, 1)]


def test_puan_jev_bayragi_varsayilan_kapali(monkeypatch):
    from video import anlamsal
    monkeypatch.delenv("VIDEO_JEV_BANT", raising=False)
    monkeypatch.setattr(anlamsal, "jev", lambda: (_ for _ in ()).throw(AssertionError("jev çağrıldı")))
    a = {"is_akisi": [{"adim": "Kullanıcı Blender'da arabanın modelini hazırlar", "zaman": "1:00", "araclar": []}]}
    assert au.puan(_rapor(**{"İş akışı": "- user prepares car model in Blender"}), a)["is_akisi"] == (1, 1)
    calisti = []
    monkeypatch.setenv("VIDEO_JEV_BANT", "1")
    monkeypatch.setattr(anlamsal, "jev", lambda: calisti.append(1) or (lambda c: [True] * len(c)))
    au.puan(_rapor(**{"İş akışı": "- user prepares car model in Blender"}), a)
    assert calisti == [1]
