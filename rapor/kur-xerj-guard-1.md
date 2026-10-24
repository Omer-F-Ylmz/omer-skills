# KUR-XERJ-GUARD-1, YARIM (A tamam, B kısmi, C/D yapılmadı)

**Sonuç:** KABUL sağlanmadı. Güvenlik kapısı geçti, XERJ düğümü ayakta; indeksleme ilk denemede hata verdi, MCP bağlantısı/guard/ölçüm yapılmadı (çağrı tavanı 45).

- A güvenlik: xerj v1.0.0-rc.98 win-x64 zip sha256 eşleşti (checksum aynı release'ten → bağımsız imza yok; exe Authenticode İMZASIZ), Defender temiz. guard v1.1.1 (tag klonu): gitleaks 0 sızıntı, semgrep 0 bulgu, skillspector `--no-llm` degraded (kesin temiz sayılmaz); manuel rg: ağ/süreç/eval yok (README ile uyumlu).
- B kısmi: `araclar/xerj/bin` (gitignore dışı, COMMIT'LENMEDİ 133 MB), düğüm `python .kos/kopru/arka.py --bagimsiz araclar/xerj/arka.log araclar/xerj/baslat.py` → 127.0.0.1:9200 200 OK, boşta ~28 MB. Not: `arka.py` bağımsız olmadan job'dan ayrılamıyor.
- Hata: `xerj autoindex C:/Projeler/omer-skills --prefix os --yes` yürüme sonunda `os error 33` (kilitli dosya) ile abort; `.xerjignore` (veri/bin/log hariç) eklendi, hâlâ aynı hata → kilitli dosya BULUNAMADI (verbose bayrağı yok). RAM boşta ~3,4 GB/32 GB.
- Kritik: XERJ `XERJ_DISABLE_FEEDBACK=true` olmadan otomatik field-report (GitHub PR) gönderiyor → her MCP/ajan ortamında bu env şart (baslat.py'de var).
- guard: README'ye göre `-p` oturumunda diyalog yerine REDDEDER (kilitlemez); sınır env `AGENT_GUARD_AGENT_MAX=7` (README tablosu doğrulanacak); plan yüzdesi API anahtarında yok. Kurulum: `/plugin install agent-usage-guard@agent-usage-guard` (etkileşimli, yapılmadı). Mod `claude -p`'de de çalışır, WSL oturumunda çalışmaz.
- Yapılmadı: Desktop/CC/ajan havuzu MCP kaydı (havuz 47801 `tools/mcp_paylasim.py PAYLASIM2` listesine "xerj" eklenip `xerj mcp` stdio→http), "Claude ile yapılanlar" indeksi, 6 görevlik jeton ölçümü, guard kurulumu+headless kanıtı, kart/zip, CLAUDE.md tek satır, tam suit.

**devam:** (1) kilitli dosyayı bul: `autoindex` alt klasör alt klasör (`skills/`, `tools/`, `docs/`, `rapor/` ayrı `--prefix`), (2) `xerj mcp` önce `claude mcp add -s user xerj -e XERJ_URL=http://127.0.0.1:9200 -e XERJ_DISABLE_FEEDBACK=true -- <tam yol>\xerj.exe mcp`, (3) guard `/plugin install`.
Maliyet ≈ $1.2 (hedef $0.50 aşıldı: çok uzun yardım/okuma çıktısı). Commit yalnız baslat.py + .xerjignore + bu rapor.
