# pulse check skill
ad: pulse check skill
tur: skill
video: zKBPwDpBfhs
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor. Kaynak kod yok. ClickUp API'ye yapılan çağrılar dışında ek telemetri bilgisi yok.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Videoda anlatılan, projeleri ve taahhütleri ClickUp'tan canlı kontrol eden bir Claude skill'i. Yayımlanmış repo yok; yalnızca video bulgusuna dayanıyor.
## Mekanizma
Video bulgusuna göre skill, ClickUp liste ID'lerini içine sabit yazıyor (hardcode). Canlı sorguyu "ClickUp searcher" alt ajanına devrediyor; alt ajan ClickUp'tan proje ve taahhüt durumunu çekiyor. Ayrıntıları (prompt, çıktı biçimi, araç çağrıları) doğrulayamadım. `video getir` komutu video kimliğiyle hata verdi, çünkü tam URL bekliyor. Bu yüzden transkripte bakamadım.
## Kanıt
- Pulse check skill ClickUp liste ID'lerini hardcode etti ve alt ajana devretti. → sınanamadı · Repo yok. `video getir zKBPwDpBfhs` komutu video kimliğiyle ValueError verdi (unknown url type), transkript alınamadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- bilinmiyor
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Proje ve taahhüt durumunu tek komutla ClickUp'tan canlı görmeyi sağlar. Sorgu alt ajana devredildiği için ana bağlam ham ClickUp verisiyle dolmaz. Bu ikinci nokta benim çıkarımım.
## Maliyet/risk
Kaynak yok, bu yüzden kod incelenemedi. Liste ID'leri sabit yazılı olduğu için başka çalışma alanında çalışmaz ve ID'ler değişirse bozulur. ClickUp API erişimi gerekir, kimlik bilgisi yönetimi belirsiz. Bulgu tek videoya dayanıyor.
## Üretilebilir
hedef_tur: skill
tarif: SKILL.md yaz: kullanıcı 'pulse check' dediğinde bir ClickUp searcher alt ajanı başlat. Alt ajan ClickUp MCP'si veya API'siyle izlenen listeleri sorgulasın (liste ID'leri hardcode yerine bir yapılandırma dosyasından okunsun). Sonuçta açık taahhütler, geciken işler ve son değişiklikler kısa bir özet olarak dönsün. Ana bağlama yalnızca özet girsin.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
## Destek
- zKBPwDpBfhs · 14:18 · Projeleri ve taahhütleri ClickUp'tan canlı kontrol eder; sabit liste ID'leri ve ClickUp searcher alt ajanı kullanır. · kanıt: Pulse check skill, ClickUp list ID'lerini hardcode etti ve alt ajana devretti.
