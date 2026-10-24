---
type: report
status: partial
tags: [yarim-a3, arac-duzeltme]
relatedTo: [base-kur-1, autoharness-fix-1, ruflo-2, headroom-1]
---
# YARIM-A3 (24.10) — araç düzeltme

- autoharness-kur-2: ZATEN BİTMİŞ — ed4fdb44; rapor/autoharness-kur-2.md, ajan kanıtı autoharness-kanit.json ($0,099), denetim a2 `ok`.
- autoharness-fix-1: BİTTİ (kanıt yeni) — hook komutu `python3 -c ... CLAUDE_PLUGIN_ROOT` biçiminde; bu oturumda `~/.claude/autoharness/requests` mtime 12:34 → 13:14:54 değişti, hiçbir tur "hook error" satırı yok. Diğer hook'lar için ayrı önce/sonra diff çıkarılmadı (DEVAM).
- "Kullanılamayan 4 araç": görev 4'ü saymıyor; zorunlu set için ölçüldü: markitdown, summarize, semgrep, gitleaks CLI `--help` OK; departman-belge kurulu; headroom-compress hiçbir yerde kurulu değil (Skill: Unknown skill) → DEVAM.
- base-kur-1 (katalog_kanca): BİTTİ — kök neden kanıtlı: betik sağlam (tools/tests 21 yeşil, taze oturumda 13.9 KB çıktı, ~0,5 sn) ama canlıda yok: `~/.claude/skills/yetenek-getir/katalog_kanca.py` yok, settings.json'da 0 "katalog" geçişi. `onay/katalog_kanca_uygula.py --kuru` plan veriyor. Test: `onay/test_katalog_kanca_uygula.py::test_kanca_canlida_kurulu` (xfail strict; kurulunca XPASS → işaret kaldırılır). Yan kök neden: envanter_2/4 zip'i repodaki ignore'lu `__pycache__`'i alıp zip_denetle'de düşüyordu (2 test kırmızı) → süzgeç eklendi, onay suiti 27 yeşil + 1 xfail.
  ÖMER: `python onay/katalog_kanca_uygula.py uygula` (settings.json değişir, yedek alır).
- ruflo-bag-1: ZATEN BİTMİŞ — 60d475d7 (MCP_TIMEOUT 240000 + KEEP listesi), 78 test yeşil.
- ruflo-2: DEVAM — ana oturum sonu damıtma + Obsidian'a birleşik yazım yapılmadı (rapor/ruflo-2 satır 51-52); tek_banka.py --kuru: 7 aday, 7 yeni, uygulanmadı. ÖMER: `python onay/ruflo_2_ders.py uygula`.
- awesome-1: ZATEN BİTMİŞ — 1b153cf1 KABUL, awesome-rehber skill'i kurulu (~/.claude/skills).
- omniroute-1: ZATEN BİTMİŞ — 1fa3732c (3/3 uçtan uca); omniroute-2 kalite kapısını geçen aile yok, kapandı. ÖMER (isteğe bağlı): OmniRoute panelinden eski cc-yedek combo'yu sil.
- ruflo-1: ZATEN BİTMİŞ — 986eb3a9 (KABUL kod ailesi); settings.json'da 3 "ogrenme" kancası var. Açık: rapor ailesine genişleme (ayrı tur).
- headroom-1: DUR sonucu (c73e7623) hâlâ geçerli — ÖMER: 0.40.0 kırıcı (HEADROOM_LICENSE); karar ver (uv aracı 0.39.1'e sabitle / masaüstü güncelleyici 0.9.30→0.9.40). Güncelleme tüm CC oturumları kapalıyken.

Sapma: test_token_4_uygula::test_uygula_geri_ve_cc_profil_tools kırmızı (bu işlerle ilgisiz, dokunulmadı). Tur sınırı (40) nedeniyle ruflo-2 ve fix-1 diff'i bitmedi. Ayrıntı: .kos/kopru/gorev-yarim-a3-devam.md
