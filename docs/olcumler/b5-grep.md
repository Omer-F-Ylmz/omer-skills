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
