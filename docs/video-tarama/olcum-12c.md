# KURULUM-12c ölçüm — video başına alt ajan token'ı

Ölçü (12b ile aynı): task-notification `<usage><subagent_tokens>` = son turun context'i (input + cache yazma + cache okuma) + toplam çıktı.
Transcript'ten doğrulandı: 4 koşuda formülle hesap ile bildirilen değer ±1k içinde.

## K0 — 12b taban (general-purpose alt ajan, model claude-sonnet-5)

| koşu | video | subagent_tokens | tur | ilk tur (cw / cr) | tur başı ort. context | toplam cw | toplam cr |
|---|---|---|---|---|---|---|---|
| süzgeçli | yp7gg8cG5wc | 140.7k | 18 | 58.7k / 9.6k | 101k | 453k | 1.38M |
| süzgeçli | 1Jb517FRX7I | 166.9k | 18 | 68.3k / 0 | 111k | 226k | 1.76M |
| tam | yp7gg8cG5wc | 166.8k | 20 | 59.0k / 9.6k | 106k | 113k | 2.01M |
| tam | 1Jb517FRX7I | 159.6k | 14 | 59.0k / 9.6k | 105k | 114k | 1.36M |

Tur sayısı 14–20; her tur tabanı (~59–68k) yeniden önbellekten okur → maliyet ≈ taban × tur. Altyazı ~5k, kareler ~2.6k: context'in <%10'u.

Taban context ad düzeyinde (`claude -p "/context"`, ana ajan; general-purpose alt ajan aynı kalemleri alır, MCP/sistem araçları orada şema olarak yüklü):

- skill listesi 41.6k (381 skill) — en büyük kalem
- sistem araçları 13.9k (ana ajanda ertelenmiş; alt ajanda tam şema)
- MCP araçları 105.2k (ertelenmiş; yalnız adları listede)
- özel ajan listesi 8.6k
- memory dosyaları 2.4k (CLAUDE.md 1.1k · RTK.md 0.15k · proje CLAUDE.md 0.3k · MEMORY.md 0.9k)
- sistem istemi 2k · hook enjeksiyonları (mesajlar) 4.8k

Kaldıraç eşlemesi: (1) dar tanım → skill/MCP/ajan listesi ve araç şemaları düşer; (2) paket.md + paralel Read → tur 14–20'den ≤4'e; (3) sabit prompt başta → paralel alt ajanlar aynı öneki önbellekten okur.

## 12c canlı (tek koşu, `claude -p`, yeni süreç; alt ajan tipi video-tarayici, model claude-sonnet-5)

| video | subagent_tokens | 12b (tam) | fark | API turu | ilk tur context (cw / cr) | toplam cw / cr | önbellek okuma oranı |
|---|---|---|---|---|---|---|---|
| yp7gg8cG5wc | 36.4k | 166.8k | −%78 | 6 | 12.7k (6.9k / 5.7k) | 37.3k / 140.3k | %79 |
| 1Jb517FRX7I | 34.4k | 159.6k | −%78 | 6 | 12.6k (12.6k / 0) | 47.0k / 123.9k | %73 |

- Hedef ≤40k: tuttu (iki video). Taban 59–68k → 12.6k (dar tanım: skill/MCP/ajan listesi ve araç şemaları yok).
- Tur: 6 API çağrısı = Read (paket + kareler paralel) · Write · Bash denetle (tür hatası) · Bash düzelt+denetle · SubagentHandback · son metin.
  İş turu 4; son iki tur harness'in dönüş mekanizması. Hedef "≤4 tur" API çağrısı sayılırsa tutmadı (tavan 6 içinde). Write ile Bash aynı mesajda gönderilmedi.
- Önbellek paylaşımı: iki alt ajan aynı mesajda başladı; ikincisi ilk turda 5.7k'yı (sistem + araç öneki) önbellekten okudu. Sabit prompt metni önbellek kırılma noktasının ötesinde kaldı.
- Girdi: paket.md ~5.6k token (metin) + kareler ~2.2k; ana ajana giden yalnız paket'in tek satırı.
- Jev: paket 0 (p_ekran önbellekte) · toplu 31 (`--istek-tavan 38`) · köprü izle 2 → 33 ≤ 40.

## Aday karşılaştırması (12b 7186aac raporu ↔ 12c; gevşek = normalize alt dizi ya da eslestir ≥0.8)

- yp7gg8cG5wc: 12/12 = %100 (12c 16 aday; yeni: barvin/number-flow, Three.js, Awwwards seviyesi).
- 1Jb517FRX7I: 12/16 = %75 (hedef %90 TUTMADI). Kaçan: "Auto memory" (12c'de "/memory (auto memory)" adıyla var → ad farkı),
  "Seçici dosya okutma", "İlerlemeyi sorgulama (by the way)", "Bypass modu kullanmama". Anlamca 13/16 = %81.
  Üç ipucu paket.md'de mevcut (grep ile doğrulandı) → kayıp girdide değil, alt ajanın aday seçiminde. 12c'de 5 yeni aday (n8n, yapılacaklar listesi / kurallı MD, …).
  Hangi kaldıraç: token kaldıraçları değil; tek koşuluk örnek, 12b'de de koşudan koşuya ad/aday oynaklığı görülmüştü. Ölçüm ücretli olduğundan yeniden koşu yok.

## Kareden okunanlar (12b ↔ 12c)

- yp7gg8cG5wc: aynı 5 an (3:35 · 6:41 · 19:10 · 21:14 · 22:15), aynı repo adları (zanwei/design-dna, ibelick/ui-skills, 14islands/r3f-scroll-rig, ai/size-limit); 12c yıldız sayılarını da okudu. 22:15'te 12b yan paneli (tempus/satus), 12c inceleme kartını (number-flow) yazdı.
- 1Jb517FRX7I: aynı 4 an (8:05 · 9:07 · 10:08 · 11:10), aynı değerler (/context 51.000/200.000, MCP 34.500, /cost, Tier 4 %75).

## Köprü `video izle`

cc-kopru, Desktop ortamı taklidiyle (MCP stdio, beyaz liste env, cwd System32) `video izle yp7gg8cG5wc "hangi skill'ler tanıtılıyor"`: exit 0 · ozet önbellekten ·
3 segment (6:09 Design DNA / UI Skills, 7:12 Lenis, 17:36) · istek 2 · görüntü Act değil → kare yok. Çalışan Desktop örneği kopru.json'u yeniden okumak için yeniden başlatma bekliyor.

## Sapmalar

- `/video-tarama` CC'de claude.ai'den senkronlanan eski kopyaya (`~/.claude/skills/synced/…/video-tarama`, 12b akışı) çözülüyor; canlı koşuda prompt repo'daki SKILL.md'yi okuttu. `dist/yukle-12c/replace/` zip'leri claude.ai'ye yüklenene dek `/video-tarama` eski akışı çalıştırır.
- Ana ajan SKILL.md'yi (headroom sıkıştırması yüzünden) birkaç Bash turuyla okudu; ölçü alt ajan olduğu için tabloya girmez. Ana ajan maliyeti $1.42 (15 tur).
