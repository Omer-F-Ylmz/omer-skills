---
name: video-uygula
description: "Video linklerinden işe yarayanı risk katmanıyla uygular: kural ve yalnız-md skill otomatik, çalıştırılabilir her şey ONAY bekler. /video-uygula url... [--tarama-atla]. Yalnız CC'de."
---

# video-uygula — tarama → değerlendirme → katmanlı uygulama

Hiçbir plugin/MCP/CLI/hook kurulmaz; settings.json, kopru.json ve global CLAUDE.md değişmez. claude.ai'de: okuma rehberi (sandbox'ta `video` yok).

## Akış (ana ajan)

```text
1. Tarama: /video-tarama akışı (skills/video-tarama/SKILL.md). --tarama-atla: bugünkü docs/video-tarama/<tarih>-toplu.md kullanılır, alt ajan taraması yok.
2. video projeler                      # docs/projeler.md: proje CLAUDE.md'lerinden 1-2 satır (mtime'la yenilenir)
3. Seçim (ana ajan): toplu tablodaki UYGULA + BEKLE adaylarından en fazla 5; ölçüt projeler.md + dört ölçüt
   (bakım · CC'de çift mi · izin kapsamı · context maliyeti). Aday başına 1 satır gerekçe. Dört ölçütte düşen: aday.md'ye `red: <gerekçe>`.
4. Araştırma: araç adayı (skill/plugin/MCP/CLI/hook/uygulama) başına bir Agent (subagent_type: aday-arastirici — sonnet), ≤3 eşzamanlı.
   Prompt tek satır: `ad: <kebab> · tür: <tür> · video: <id> · ipucu: <tablodaki ne işe yarar / link>`. Çıktı docs/kurulumlar/adaylar/<ad>.md.
   İpucu/iş akışı adayında araştırılacak repo yok: aday.md'yi ana ajan yazar (alanlar: ad · tur · video · kural: <tek cümle kural>).
5. video katman docs/kurulumlar/adaylar/<ad>.md... [--yeniden] [--istek-tavan M]
6. Sohbete katman çıktısı (≤20 satır) + seçim gerekçeleri.
```

## Katmanlar (`video katman`, deterministik)

- Kayıtta (docs/kurulumlar/kayit.jsonl) olan ad atlanır; `--yeniden` zorlar.
- T0 ipucu/iş akışı: 12f kural karşılaştırması (≤2 Jev/aday); çiftse eklenmez, değilse C:\Projeler\omer-kurallar.md'ye `N. <kural> (video <id>, 14a)`. Global CLAUDE.md'ye yazılmaz, rapora öneri satırı düşer.
- RED: `red:` alanı · lisans MIT/Apache-2.0/BSD/0BSD/ISC/CC-BY-4.0 değil ya da yok · arşivli · son commit >12 ay · skill'de SkillSpector koşmadı ya da HIGH/CRITICAL >0.
- T1 skill: kaynak klasörü gerçekten listelenir; yalnız .md (+LICENSE/NOTICE) → skills/<ad>/ + LICENSE + KAYNAK.md (repo@commit) + dist/yukle-14/yeni/<ad>.zip + skill_denetim; denetim hatası → geri alınır, T2.
- T2 geri kalan her şey: docs/kurulumlar/bekleyen/<ad>.md (`# ONAY <ad>` + aday.md: kurulum · duman testi · geri alma · köprü izni). Komut koşulmaz; Ömer "ONAY <ad>" derse Kurulum bloğu elle koşulur.
- Kayıt satırı: {ad, katman, karar, tarih, video, kaynak_commit, geri_alma}.

## Aday dosyası (≤40 satır)

Başta alan satırları: `ad · tur · video · repo · lisans (SPDX|yok) · son_commit · arsiv · kaynak (yerel skill klasörü|yok) · kural (ipucu) · red (isteğe bağlı)`.
Bölümler: Ne · Kanıt · Kurulum · İzinler · Duman testi · Geri alma · Köprü izni (yalnız salt-okur alt komutlar) · Önerilen katman.

## Tavanlar

Jev: tarama önbellekten 0; katman ipucu başına ≤2. Araştırıcı alt ajan ≤5. Çıktı: OTOMATİK UYGULANDI · ONAY BEKLİYOR · YÜKLENECEK ZIP · RED · CLAUDE.md önerisi.
