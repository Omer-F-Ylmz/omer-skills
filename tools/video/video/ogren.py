"""15 öğrenme: durum.md · karar kümesi · kural/olgu · bilgi kartı · çelişki · sponsor · bizde durum."""
ELLE = "<!-- elle -->"
TAVAN = 3000
KARAR = ("KUR", "DENE", "ÖĞREN", "ZATEN VAR", "ALTERNATİF", "RED")
TUR_SORU = "Videodaki ipucu (state) Ömer'in iş akışına dair bir davranış kuralı mı, yoksa model/araç/ortam hakkında bir olgu mu?"


def yargi_oku(k):
    raise NotImplementedError


def kart_metni(a, bugun):
    raise NotImplementedError


def kart_denetle(metin):
    raise NotImplementedError
