# GOAT Projesi Bölüm 1: Tek Başına Çalışan Bir Ekip Kuruyoruz (Super Agent)
kanal: Burhan KOCABIYIK · süre: 9 dk · altyazı: otomatik tr
ana iddia: GOAT, Claude Code üzerinde yönetici + uzman ajanlardan oluşan "tek ajan orkestrası" ile ajans kurulumundan lead bulma, e-posta ve teklife kadar işi otonom yapacak (açık kaynak + cloud); bölüm geliştirme vlog'u, ürün henüz bekleme listesinde.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Apify | YENİ | ELENDİ | GOAT'ın lead veri kaynağı; API token + ücretli kullanım, lead kazıma iş kapsamı dışı |
| DuckDuckGo arama | ÇİFT | ELENDİ | Apify token yoksa ücretsiz yedek arama; agent-reach (Exa) / Claude Code WebSearch ile aynı iş |
| GOAT (goatstarter.com) | YENİ | ELENDİ | yalnız bekleme listesi; açık kaynak sürüm yayınlanmadı, demoda hâlâ hata var |
| Yönetici ajan + uzman çalışan ajanlar + kontrol ajanı (ekran görüntüsüyle doğrulama) | ZATEN VAR | ELENDİ | Claude Code subagent'ları + superpowers:subagent-driven-development; ekran görüntüsü kontrolü frontend-craft Bölüm 2/9 |
| diğer: hata alan aşamadan sonrakine geçmeme, çoklu terminalde paralel oturum | ZATEN VAR | ELENDİ | CLAUDE.md DUR raporu; superpowers:using-git-worktrees + dispatching-parallel-agents kurulu |
| Alt-ajan tarifinde iyi çıktı örneği + kural listesi + kontrol | YENİ | BİLGİ | kural listesi ve doğrulama CLAUDE.md'de var; ajan başına "iyi örnek" şartı yok |
| diğer: Instantly?, fal.ai, Manus?, DOA (Skool), Gumroad ürünleri | YENİ | ELENDİ | ücretli API/hesap ya da reklam/kurs; kullanım gösterilmedi, iş kapsamı dışı |
## ölçütler (YENİ)
- Apify: bakım=bilinmiyor (servis, repo belirtilmedi) · çift=kısmen agent-reach (Exa arama/Jina okuma), lead kazıma yok · izin=API token + ücretli hesap · context=kurulmadı, yalnız GOAT içinde çağrılınca · kurulum: —
- GOAT: bakım=bilinmiyor (repo yayınlanmadı) · çift=örtüşme yok · izin=bekleme listesi hesabı + Apify/Instantly/fal anahtarları · context=bilinmiyor (yayınlanmadı) · kurulum: —
- Alt-ajan tarifinde iyi örnek: bakım=yok (teknik) · çift=CLAUDE.md hedef-güdümlü/kabul kriteri kısmen · izin=yok · context=CLAUDE.md'ye tek satır, her oturum · kurulum: —
- diğer (Instantly?, fal.ai, Manus?, DOA, Gumroad): bakım=bilinmiyor (servis/ürün, repo yok) · çift=örtüşme yok · izin=API anahtarı/ücretli hesap ya da topluluk/kurs üyeliği · context=kurulmadı, sıfır · kurulum: —
## hedefler (BİLGİ)
- Alt-ajan/aşama tarifine en az bir iyi çıktı örneği + kural listesi + kontrol adımı koy → CLAUDE.md (CONTEXT DİSİPLİNİ: subagent delegasyonu)
---
## ek: somut
- ayar: GOAT onboarding alanları: kurucu adı, ajans adı, sektör ("sen seç" ile yönlendirme), şehir (demo: Esat · Doğa Ajans · İstanbul)
- ayar: GOAT aşama anahtarları: Apify token (lead tarama/puanlama) → Instantly? (e-posta gönderimi) → fal (görsel, rapor, teklif grafikleri); Apify yoksa ücretsiz DuckDuckGo aramasına düşüyor
- komut: terminal komutu gösterilmedi; Claude Code'a verilen istem: "hata alınca sonraki aşamaya geçmesin", "arada site yap deyince yapabilsin", "daha robust yap"
- dosya: yok
- sayı: Apify veri maliyeti 35 sent — yalnız iddia
- sayı: proje 2 hafta önce başladı; seri 3 bölüm — yalnız iddia
- sayı: 3 terminal paralel çalışıyor (bir ekranda 2) — gösterildi (altyazıya göre ekranda)
- sayı: Apify token verilmeyince 0 lead — gösterildi (canlı demo hatası)
- sayı: DOA-zero kaynakları %100 ücretsiz — yalnız iddia (açıklama)
