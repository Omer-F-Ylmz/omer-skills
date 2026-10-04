# Motor formları (MOTOR-M1 K4 taslak)

Model adımları serbest metin değil **form** (JSON Schema) döndürür; rapor ve aday.md koddan üretilir. K3'te `--json-schema` ile 4/4 hafif çağrı ilk denemede geçerli form verdi (CC şemayı StructuredOutput aracıyla zorluyor).

## Red kuralı
- Form kodda JSON Schema ile doğrulanır. Zorunlu alan eksik ya da boşsa (`minLength: 1`; "neden/ne" alanları boş dize olamaz) **form reddedilir** ve aynı çağrı hata listesiyle **yeniden istenir** (en fazla 2 yeniden istek).
- Üçüncü red: `durum.json` adımı `form_red` olur, karar paneline düşer; parti diğer videolarla devam eder.

## 1. Tarayıcı formu (video başına, tam tarama)
```
video:        {id, baslik, sure_s, short: bool}                      # koddan doldurulur (paket künyesi)
ozet:         str!                                                    # 2-4 cümle
bolumler:     [{zaman!, baslik!}]
adaylar:      [{ad!, tur! (skill|plugin|mcp|cli|hook|araç|site/ui|prompt|iş akışı|ipucu),
                ne!, kanit_zamani (m:ss; açıklamadaysa ""), kaynak! (altyazı|kare|açıklama),
                repo_url|null, iddialar: [str]}]
aciklama_baglantilari: [{url!, ne!, aday_mi! bool, neden!, aday_adi|null}]   # HER bağlantı için zorunlu
site_ui:      [{teknik!, ne!, kanit_zamani!, kaynak!}]                # Site/UI referans teknikleri
promptlar:    [{metin!, amac!, kanit_zamani!, kaynak!}]
iddialar:     [{iddia!, kanit_zamani!, kaynak!, aday_adi|null}]
kareden_okunanlar: [{kare!, okunan!}]
belirsizlikler: [str]
iz:           [{kaynak!, ne!, baglandigi!, kanit!}]   # D1 (b): her bahis bir satır; baglandigi = aday adı ya da "aday değil: <sabit sebep>"; yoksa rapor şema 1
```
`!` = zorunlu ve boş olamaz. `atlanan_segment_orani` modelden istenmez; kod paketteki segment sayısından hesaplar. Kod ayrıca `aciklama_baglantilari` sayısının paketteki bağlantı sayısına eşit olduğunu denetler (eksikse red).

## 2. Araştırıcı formu (araç başına, tek derin araştırma)
```
ad!, tur!, repo_url|null, lisans! (SPDX|"yok"|"bilinmiyor"), yildiz|null, son_commit|null,
ne!, kurulum: [adim!], skillspector|null (tür skill ise zorunlu),
iddia_sinama: [{iddia!, sonuc! (doğrulandı|çürütüldü|sınanamadı), kanit!}],
ozellikler: [{ozellik!, kaynak_url!}],
destek: [{video!, zaman!, bulgu!}]           # koddan eklenir: her videonun tarayıcı formundan
video_ozgu_ozellik: [{video!, ozellik!, arastirma!}]   # önceki araştırmada olmayan özellik için ek çağrı
```

## 3. Mevcut rapor biçimine eşleme
| Mevcut bölüm (docs/video-tarama/*.md) | Form alanı | Üreten |
|---|---|---|
| Künye | video | kod (paket) |
| Özet | ozet | model |
| Bölümler | bolumler | model |
| Adaylar | adaylar + aciklama_baglantilari (aday_mi=true) | model |
| Site/UI referans (24e-2) | site_ui | model |
| İddialar | iddialar | model |
| Kareden okunanlar | kareden_okunanlar | model |
| Belirsizlikler | belirsizlikler | model |
| Atlanan segment oranı | — | kod |
| (yeni) Prompt'lar | promptlar | model |

| Mevcut aday.md (docs/kurulumlar/adaylar/) | Form alanı |
|---|---|
| ad · tur · video · etiket · kural (ön bilgi) | ad · tur · destek[0].video · kod (etiket) · karar sonrası kod (kural) |
| ## Ne | ne |
| ## Kanıt | destek (video · zaman · bulgu) |
| ## İddia sınama | iddia_sinama |
| repo metası · kurulum · SkillSpector (aday-arastirici tanımı) | repo_url · lisans · yildiz · son_commit · kurulum · skillspector |

`video rapor-denetle` ve `ajan-denetle` kuralları M2'de form doğrulamasına taşınır; md çıktısı mevcut denetimi değişmeden geçmelidir (M2 kabul kriteri).
