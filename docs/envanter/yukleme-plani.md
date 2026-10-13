# ENVANTER-1 yükleme planı (d1 öneri; uygulama + ölçüm d2)

İlke: envanter bilgisi CLAUDE.md'ye dökülmez. Bağ noktası iki yer: (a) departman-* SKILL.md sonundaki `## Dizin` (SKILL-SEÇİM, kol/secim d6 KABUL biçimi: `ad: ≤8 kelime`, yalnız opak adlar, üreteç `tools/secim/dizin_uret.py` + `tools/secim/anahtar.json`); (b) departmansız işler için tek yeni müdür. Kurulu hiçbir şey kaldırılmaz.

## A. CC tarafı (Dizin'e ek)
1. `is-arac.md` §1 "eklenecek" sütunundaki MCP/CLI/plugin adlarını `anahtar.json`'a görev ifadesiyle ekle → `dizin_uret.py` ile 12 Dizin'i yeniden üret (elle yazma yok). Tahmini artış: departman başına 2–5 satır, toplam ≲2 KB.
2. Departmanı olan önekli ajanlar (db 22, fe 19, qa 18, be 15, sec 15, pln 14, inc 12, dok 11, ara 9 = 135): Agent aracı açıklamaları zaten oturum listesinde → Dizin'e EKLENMEZ (d5 bulgusu: CC'de ajan Dizin satırı fayda etmiyor). Yalnız `departman-*/ajanlar/` kopyası yoksa ekle (claude.ai için).
3. Kendi plugin'lerinin CC sürümü eski: `blender` 1.1.0 → repo 1.3.0, `frontend-craft` 1.5.7 → repo 1.9.0. Bunlar envanter değil, bekleyen onay betikleri (BLENDER-4, TASARIM-3); Ömer koşar.

## B. Departmansız işler: `departman-diger` (1 kayıt)
- `is-arac.md` §2 tablosu (11 iş türü) SKILL.md gövdesi olur (≤40 satır), `ajanlar/` altına departmansız önek ajanları kopyalanır: ops 29, dil 26, ml 23, urn 20, otm 9, mob 8, oyn 4, vid 4 = 123 tanım.
- Açıklama: "Video, Blender/3D, oyun/mod, görsel üretim, otomasyon, hukuk, pazarlama, bulut, ML, mobil işlerine başlarken önce oku."
- `docs/departmanlar/diger.md` (mevcut, 757 B) katalog olarak bağlanır.
- d2 seçim testi bu tek müdürde düşerse 11 iş türü 3–4 aileye bölünür (medya: video+3D+görsel · üretim: otomasyon+oyun+mobil · iş: hukuk+pazarlama · altyapı: bulut+ML).

## C. claude.ai 1000 kayıt sınırı — aile paketi
Şu an claude.ai'de 591 skill (13 Eki 13:40; boş yer 409). Öneri ("kullanabilelim" önceliği: yalnız işe yarayan gider):

| Paket | İçerik | Kayıt | Gerekçe |
|---|---|---|---|
| `departman-diger` (B) | 11 iş türü + 123 ajan tanımı | +1 | claude.ai'de alt ajan yok; 123 uzman talimat olarak okunur |
| Mevcut 12 `departman-*` zip'i | Dizin + `ajanlar/` (207 tanım) | 0 (değiştir) | SKILL-SEÇİM d6 zip'leri hazır (dist/skill-secim-1/kendi, kol/secim), yükleme bekliyor |
| Yalnız CC 512 yerel skill | 45 günde yalnız 3'ü kullanıldı: `make-pdf`, `plan-ceo-review`, `threejs-bloom` | +3 | Toplu yükleme yok; kullanılanlar tek tek |
| Plugin skill'leri (912 kopyasız) | CC'de kullanılan 5'i (`chrome-devtools`, `context-mode`, `figma`, `frontend-design`, `review`) MCP'ye bağlı | 0 | claude.ai'de MCP yok → yükleme işe yaramaz; `frontend-design` yerine `frontend-craft` zaten orada |
| Ajan aileleri ayrı ayrı (8 × aile-*) | yalnız B'nin d2'de düşmesi halinde | +8 | yedek plan |

Toplam: +4 kayıt (595/1000). 1000'e yaklaşılırsa aynı aileden ≥5 claude.ai skill'i tek "aile" skill'ine (SKILL.md dizin + `references/<ad>.md`) katlanır; aday aileler `bosluk.md` §2 öbek sayımından.

## D. Desktop MCP eşitliği
- Yalnız CC 46 MCP; Desktop'a taşınması gereken yok sayılmaz — Desktop ihtiyacı `cc-kopru` (31 izinli CLI) üzerinden. Yalnız gerçekten kullanılan ve yerel yolu olmayanlar adaydır: `context7`, `mslearn`, `21st`, `nano-banana-2` (son 45 günde CC'de çağrıldı). Ekleme Desktop yapılandırması = canlı ayar → onay betiğiyle, Ömer kararı.
- claude.ai bağlayıcıları CC'den görünmüyor; envanterdeki 7 ad yalnız `mcp-needs-auth-cache`. Tam liste için Ömer claude.ai Ayarlar > Bağlayıcılar ekranını bir kez kopyalar → `topla.py`'a elle liste girdisi (d2).

## E. d2 ölçüm kapısı
- Skill seçim testi (`tools/secim/secim_gorevler.json`, `secim_olc.py toplu`): doğruluk ≥ taban (186/196) VE çağrı başı jeton ≤ taban. Yeni görevler: §2'nin 11 iş türünden birer görev (beklenen = tablo ilk aracı).
- Çağrı tavanı: en fazla 12 `claude -p` (taban + sonra × ana/zor/web), plan limiti, API anahtarı alt sürece verilmez.
