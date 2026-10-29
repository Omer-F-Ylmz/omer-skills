# ENVANTER-DOGRULA-1
- Girdi kurtarma: 279 kayıp değildi, tsv'ye yazılmamıştı. `ogren/yeni1-cikti/env*.tsv` ham çıktısından `yeni1_birlestir.py` mantığıyla (ad,tür) tekilleştirilince 1043 satır geri çıktı; bunların 279'u eski kaba ad-alt-dize eşleşmesiyle "KURULU" idi (tsv'ye yalnız 764 KURULACAK yazılmıştı).
- Tekilleştirme: repo slug (owner/repo) > normalize ad → 1043 satır → **955 tekil**.
- Sonuç (955 tekil): **KURULU-KANIT 174 · KURULACAK 703 · BELİRSİZ 78**
- KURULU-KANIT: 40 repo-URL eşleşmesi (installed_plugins/known_marketplaces/araclar+indirilen git remote/kayit.jsonl KUR), 134 ad eşleşmesi (~/.claude/skills, plugin cache, araclar/, C:\AI\indirilen, _inv_* mcp/npm/pip/uv/winget/plugin/skills, envanter.tsv CC/ikisi/claude.ai, ~/.claude.json mcp adları). Kanıt yolu her satırda `kanit` sütununda.
- BELİRSİZ: yalnız benzer (≥7 harf, ≥%60 örtüşen) ad ya da yalnız katalog (yetenek.tsv) eşleşmesi; aynı araç mı doğrulanmadı. Model/CLI ile `--version` doğrulaması yapılmadı.
- Sınırlar: ad eşleşmesi 134 satırda aynı-araç garantisi vermez (repo URL'si yok); `where`/`--version` ve mcp list canlı sınanmadı; YANLIŞ EŞLEŞME/KISMEN ayrımı yapılmadı (BELİRSİZ'e düştü). Eski 279 kaba "kurulu"nun tekil karşılığı: 955 içinde 174 kanıtlı.
- Çıktı: `rapor/video-yeni-1-kurulacaklar-tekil.tsv` (sınıf sıralı). Betik: tmp/ed1_b.py. Kurulum yapılmadı.
