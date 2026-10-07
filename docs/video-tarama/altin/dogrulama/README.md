# Altın küme — Desktop doğrulaması (2026-10-07)

Her video için CC'nin Sonnet taslağı, ham dökümlerin tamamına (açıklama, yorum, YouTube altyazısı, Groq dökümü, 1080p OCR) karşı bağımsız olarak yeniden kuruldu. Değişiklik günlükleri: `<id>.md` (taslaktan çıkarılan aday yok; eklemeler kaynak + zaman + kanıtla).

## Şema kararları
- `adaylar` yalnız adlandırılmış varlıklar: skill · plugin · MCP · CLI · kütüphane · uygulama · servis · model · font · adı konmuş teknik. Ad eşleşmesiyle puanlanır.
- `ogrenimler` (yeni alan): betimsel bulgular — ipucu, iş akışı kuralı, anlatılan teknik. Kelime örtüşmesiyle puanlanır (site_ui ile aynı kural); adla eşleşemezler.
- `belirsiz: true` olan aday paydaya girmez; bulunursa ayrıca "belirsiz bulundu" olarak sayılır (ekranda görünüp kullanılmayan menü öğeleri, dock simgeleri vb.).
- Sponsor yalnız açık ifadeyle: 1nGx7WR8YLE açıklaması "Bu video Topview sponsorluğunda üretilmiştir" → topview.ai linki sınıf sponsor, aday true (araç da videoda kullanılıyor).

## Sayılar (taslak → doğrulanmış)
| video | adaylar (belirsiz) | ogrenimler | site_ui | promptlar | komutlar | urller | is_akisi | linkler |
|---|---|---|---|---|---|---|---|---|
| aZe5ZTYcF1M | 3 → 23 (1) | 22 | 4 → 23 | 1 → 3 | 0 → 1 | 1 → 3 | 3 → 14 | 2 |
| 1nGx7WR8YLE | 11 → 23 (5) | 14 | 3 → 10 | 2 → 8 | 0 | 2 → 5 | 6 → 12 | 2 |
| YDAK1lvVXho | 9 → 31 (5) | 9 | 6 → 18 | 1 → 4 | 0 | 1 → 2 | 3 → 15 | 1 → 2 |
| FaChtkkG9X4 | 5 → 17 (1) | 1 | 2 → 20 | 5 → 6 | 1 | 4 → 6 | 6 → 15 | 4 |
| d_UE-wHLoZY | 5 → 26 (13) | 1 | 1 → 2 | 0 → 2 | 0 | 1 | 6 → 15 | 1 |

Taslak altın, gerçeğin yaklaşık üçte birini tutuyordu; taban puanları bu yüzden olduğundan iyi görünüyordu.
