# prompt-hilesi (DZkZtw2icLq)

**Amaç:** Claude Code'da Fable 5 benzeri davranış yeniden oluşturma.
**Araçlar:** GitHub (CL4R1T4S repository), Claude Code (Opus 4.8 Max model), Terminal komutları (--System-prompt-file)

**Adımlar**
1. [] GitHub'dan CLAUDE-FABLE-5.md dosyasını indirin.
2. [] Indirilen prompt dosyasını Claude Code projenizin src klasörüne kopyalayın.
3. [] Terminal'de `claude --dangerously-skip-permissions --System-prompt-file CLAUDE-FABLE-5.md` komutunu çalıştırarak prompt'i yükleyin.
4. [] Opus 4.8 Max modelini aktif model olarak seçin.
5. [] Apple tarzı landing page prompt'ini kullanarak test sonucunu karşılaştırın.

**Prompt/kod/ayar:** --System-prompt-file CLAUDE-FABLE-5.md
**Sonuç:** Apple tarzı landing page prompt'inde daha iyi visual hiyerarşi, polish ve execution elde edildi.
**Bizde (öneri, modelden):** Kurulu Claude Code ve Opus 4.8 Max modeli ile aynı prompt dosyasını yükleyerek test edebilirsiniz.
**Daha iyi (öneri):** Daha iyi sonuçlar için prompt dosyasını düzenleyebilir veya farklı test prompt'leri deneyebilirsiniz.
