YARIM-A3-DEVAM — kalan adımlar (rapor/yarim-a3.md)

1. autoharness-fix-1: ~/.claude/settings.json + ~/.claude.json hook listesinin önce/sonra diff'i (dotnet-format, block-destructive, rtk, claude-mem, ruflo, autoharness); yamanın plugin güncellemesinde kaybolmaması için .kos/kopru/autoharness_winfix.py'yi repoya (tools/) al.
2. headroom-compress: kurulu değil (Skill Unknown; headroom-marketplace plugin'inde skill yok). Zorunlu araç listesinde tutulacaksa kaynağını bul/kur ya da listeden çıkar (zorunlu_arac).
3. ruflo-2: tools/ruflo/tek_banka.py --kuru → uygula (Obsidian 50-dersler birleşik yazım); ana oturum sonu damıtma tasarımı (SessionEnd kancası); ÖMER: python onay/ruflo_2_ders.py uygula.
4. base-kur-1: ÖMER onayıyla `python onay/katalog_kanca_uygula.py uygula`; sonra test_kanca_canlida_kurulu'daki xfail işaretini kaldır.
5. onay/test_token_4_uygula.py::test_uygula_geri_ve_cc_profil_tools kırmızı (YARIM-A3 öncesi ya da ilgisiz; kök neden bakılmadı).
Kanıt: ajan-sira/{autoharness-fix-1-a2,ruflo-2-d4,base-kur-1-a2}.json
