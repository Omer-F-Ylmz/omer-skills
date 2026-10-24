# VIDEO-REPO-3 (düzeltme): repo = zycck/claude-mods
rapor/video-repo-3.md "BULUNAMADI" diyor; ekran karesi OCR'ı onu çürütüyor.
- Kanıt: docs/video-tarama/derin/U6xZX4YWFkU.json ekran[] kare 0005: `gthub.com/zycck/eiaude-mods` (bozuk OCR = github.com/zycck/claude-mods) + "Progress", "Plan in canlı ilerleme çubukları".
- Transkript 168,5-170,2 sn: "a mod that turns Claude's plan into live progress bars on the prompt" = repo açıklaması "live plan progress bars above the prompt".
- Repo: MIT, tek eklenti `plan-progress` (HEAD b77335ee, 14 dosya: hooks.json, register.tsx, SKILL.md, 3 wav, testler). Safe-delete/next-steps/cache-clock bunda yok (onlar videoda prompt ile yazdırılan örnekler) — diğer rapor yalnız bu üç adı aradığı için zycck'i elemişti.
- Güvenlik kapısı: gitleaks temiz. skillspector/semgrep dönmedi (süreç durduruldu) → kurulum YAPILMADI. Klon: .kos/kopru/ara/vr3/zycck.
- Devam: skillspector + semgrep (arka.py), temizse kur; video-kur-1-p1.tsv/kacan-karar.tsv `zk/claude-mods` → `zycck/claude-mods`.
- Bütçe aşıldı (~$1,3): CPU OCR uzun sürdü; kanıt ilk JSON'daydı.
