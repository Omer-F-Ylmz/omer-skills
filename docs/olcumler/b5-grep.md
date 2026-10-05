# B5 grep ölçümü — tools/jev (5 Eki, O29)
Komut: `uy.mekanizma(..., Path('C:/Projeler/omer-skills/tools/jev'), 'omer/jev')`, `MEKANIZMA['satir']` sınırsız (tüm eşleşmeler), yerel, ağsız.
Yanlış eşleşme gözle sayıldı (yanlış = o kategorinin mekanizması değil: belge/yardım dizesi, yorum, test, .venv, istisna sınıfı).

| kategori | önce satır | önce yanlış | sonra satır | sonra yanlış |
|---|---|---|---|---|
| oturum başı enjeksiyon | 6 | 5 (cli.py:280 help dizesi · skill.py:28 belge dizesi · skill.py:244 docstring · 2 test) | 3 | 2 (cli.py:280 · skill.py:28) |
| hook | 1 | 1 (skill.py:29 belge dizesi) | 1 | 1 (aynı) |
| süreç | 2 | 2 (test) | 0 | 0 |
| ağ | 16 | 10 (6 .venv yorum URL · cekirdek.py:130 import urllib.error · :137 except · 2 test) | 3 | 0 |
| izin kapsamı | 0 | 0 | 0 | 0 |
| ayar okuma | 11 | 5 (3 .venv · skill.py:28 belge dizesi · 1 test) | 7 | 1 (skill.py:28) |
| ağır döngü | 0 | 0 | 0 | 0 |
| **toplam** | **36** | **23 (%64)** | **14** | **4 (%28,6)** |

Kalan yanlışların hepsi kod içindeki belge/yardım dizeleri (skill.py:28–29 HOOK_AYAR, cli.py:280 help=) — satır tabanlı grep dizeyi koddan ayıramaz.
Kayıp: cekirdek.py:19/37/39 uç nokta sabitleri (çıplak URL) artık "ağ"da yok; çağrı yeri (cekirdek.py:131–135) görünüyor.
Karar (plan kuralı): yanlış %28,6 > %20 → sıradaki madde semgrep geçişi (çevrimdışı: --metrics=off --disable-version-check).

## semgrep (5 Eki, O31) — kabul ölçümü
Komut aynı (gerçek semgrep, yerel, ağsız, `MEKANIZMA['satir']` sınırsız); çıktı dosyaya yazıldı, süzülmedi. Süre: 5,4 sn (semgrep + kalan grep yolu).
Ölçümde bulunan hata: Windows'ta semgrep yml'i cp1252 okur → message bozuk (`aÄŸ`, `uÃ§ noktalar`) → 14 sonuçtan 8'i sessizce atıldı
(önce 6 satır görünüyordu). Düzeltme: kategori kural kimliğinden (check_id) çözülür; aşağıdaki sayılar düzeltme sonrası.

| kategori | grep sonra satır | grep sonra yanlış | semgrep satır | semgrep yanlış |
|---|---|---|---|---|
| oturum başı enjeksiyon | 3 | 2 | 1 (skill.py:272) | 0 |
| hook | 1 | 1 | 0 | 0 |
| süreç | 0 | 0 | 0 | 0 |
| ağ | 3 | 0 | 2 (cekirdek.py:133/135) | 0 |
| izin kapsamı | 0 | 0 | 0 | 0 |
| ayar okuma | 7 | 1 | 6 (cekirdek:180 · cli:282 · skill:74/93/118/307) | 0 |
| ağır döngü | 0 | 0 | 0 | 0 |
| uç noktalar | — | — | 4 (cekirdek.py:19/37/39/41) | 0 |
| **toplam** | **14** | **4 (%28,6)** | **13** | **0 (%0)** |

Sınırda 2 satır doğru sayıldı: cekirdek.py:41 `"url": MCP_URL` (semgrep sabit yayılımı; tanım değil kullanım yeri) · skill.py:118 settings.json
yalnız mtime için. İkisi yanlış sayılsa 2/13 = %15,4. Belge/yardım dizeleri (skill.py:28–29, cli.py:280) artık eşleşmiyor.
Karar: yanlış < %20 → semgrep yolu kabul.
